from langgraph.graph import StateGraph, END

from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda

from typing import Dict, TypedDict
import re
import pandas as pd
import ccxt


client = ccxt.bybit()

# Define state
class AgentState(TypedDict):
    question: str
    facts: list
    conclusion: str
    

# LLM
llm = ChatOllama(model='qwen2.5:3b')


def extract_symbol(question: str) -> str:
    match = re.search(r'\b[A-Z]{1,5}\b', question)
    return match.group(0) if match else None


def get_data(symbol: str):
    data = client.fetch_ohlcv(symbol, '1h')

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('timestamp', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index.tz_localize('UTC').tz_convert('Africa/Cairo')

    return df


## Calculate RSI
def rsi(data: pd.DataFrame, period: int):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = pd.DataFrame()
    rsi['RSI'] = 100 - (100 / (1 + rs))
    rsi.dropna(inplace=True)

    return rsi

def macd(data: pd.DataFrame, fast_preiod: int, slow_period: int, signal_period: int):
    slow_ema = data['close'].ewm(span=slow_period, adjust=False).mean()
    fast_ema = data['close'].ewm(span=fast_preiod, adjust=False).mean()

    macd = pd.DataFrame()

    macd['macd'] = fast_ema - slow_ema
    macd['macdSignal'] = macd['macd'].ewm(span=signal_period, adjust=False).mean()
    macd['macdHist'] = macd['macd'] - macd['macdSignal']

    macd.dropna(inplace=True)

    return macd

## Calculate Bollinger-Bands
def bbands(data: pd.DataFrame, period: int):
    bbands = pd.DataFrame()
    # Calculate the 20-period Simple Moving Averages (SMA)
    bbands['SMA'] = data['close'].rolling(window=period).mean()

    # Calculate the 20-period Standard Deviation (SD)
    sd = data['close'].rolling(window=period).std()

    # Calculate the Upper Bollinger Band (UB) and Lower Bollinger Band (LB)
    bbands['UB'] = bbands['SMA'] + 2 * sd
    bbands['LB'] = bbands['SMA'] - 2 * sd

    # bbands = pd.concat([upper, lower], axis=1, names=['UB', 'LB'])
    # bbands.dropna(inplace=True)

    return bbands

def compute_technical_indicators(data: pd.DataFrame) -> Dict[str, str]:
    if data.empty:
        return {"Error": "No price data available"}
    
    data = pd.concat([data, rsi(data, 14), bbands(data, 20), macd(data, 12, 26, 9)], axis=1, )
    return {
        "Last-Price": f"{data['close'].iloc[-1]:.2f}\n",
        "RSI": f"${data['RSI'].iloc[-1]:.2f}\n",
        "Bollinger-Bands": f"Upper-Band: ${data['UB'].iloc[-1]:.2f} --- Lower-Band: ${data['LB'].iloc[-1]:.2f}\n",
        "MACD": f"MACD: {data['macd'].iloc[-1]:.4f} --- MACD-Signal: {data['macdSignal'].iloc[-1]:.4f} --- MACD-Hist: {data['macdHist'].iloc[-1]:.4f}\n"
    }
    

def gather_facts(state: AgentState) -> AgentState:
    symbol = state['question']
    
    if not symbol:
        state['facts'].append("Error: Could not extract ticker from question.")
        return state

    data = get_data(symbol)
    
    fundimental = client.fetch_ticker(symbol) or {}
    
    facts = [
        f"Latest Closing Price: ${data['close'].iloc[-1]:.2f}",
        f"Percentage: {fundimental['percentage']}",
        f"Change: {fundimental['change']}",
        f"quoteVolume: {fundimental['quoteVolume']}",
        
    ]
    facts += [f"{key}: {value}" for key, value in compute_technical_indicators(data).items()]
    
    state['facts'].append('\n'.join(facts))
    
    return state

def draw_conclusion(state: AgentState) -> AgentState:
    facts = '\n'.join(state['facts'])
    
    prompt = PromptTemplate(template="""Based on these financial facts:
    {facts}
    Provide a structured analysis of the CRYPTO's potential movement:
    \n- **Trend Analysis**\n\n
    
    \n- **Market Position**\n\n
    
    \n- **Potential Risks**\n\n
    
    and show answers in separate it structered analysis
    """, input_variables=["facts"])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({'facts': facts})
        
        # Extract only the content from the response
        if hasattr(response, 'content'):
            state['conclusion'] = response.content
        else:
            state['conclusion'] = str(response)
    
    except Exception as e:
        state["conclusion"] = f"Error in conclusion generation: {str(e)}"
    
    return state

workflow = StateGraph(AgentState)
workflow.add_node("gather_facts", gather_facts)
workflow.add_node("draw_conclusion", draw_conclusion)
workflow.add_edge("gather_facts", "draw_conclusion")
workflow.add_edge("draw_conclusion", END)
workflow.set_entry_point("gather_facts")
graph = workflow.compile()