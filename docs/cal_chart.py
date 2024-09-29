from pymongo import MongoClient
import pandas as pd
import ta  # 기술적 지표 라이브러리
def cal_chart():
    # MongoDB에 접속
    mongoClient = MongoClient("mongodb://localhost:27017")
    # 'bitcoin' 데이터베이스 연결
    database = mongoClient["bitcoin"]
    # 'chart_15m' 컬렉션 작업
    chart_collection = database['chart_15m']

    # 최신 데이터 200개만 가져오기 (timestamp 내림차순 정렬)
    # data_cursor = chart_collection.find().sort("timestamp", -1).limit(200)
    data_cursor = chart_collection.find().sort("timestamp", -1)


    # MongoDB 데이터 DataFrame으로 변환
    data_list = list(data_cursor)
    df = pd.DataFrame(data_list)

    # 타임스탬프를 datetime 형식으로 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 불필요한 ObjectId 필드 제거
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)

    # 인덱스를 타임스탬프로 설정
    df.set_index('timestamp', inplace=True)

    # 시간순으로 정렬 (오름차순)
    df.sort_index(inplace=True)

    # 열 이름 확인 (예: ['close', 'high', 'low', 'open', 'volume'])
    print("데이터 컬럼명:", df.columns)

    # 데이터프레임 출력 (정렬된 상태로 확인)
    print(df.head())

    # 1. MACD (Moving Average Convergence Divergence)
    df['macd'] = ta.trend.macd(df['close'])
    df['macd_signal'] = ta.trend.macd_signal(df['close'])
    df['macd_diff'] = ta.trend.macd_diff(df['close'])

    # 2. RSI (Relative Strength Index)
    df['rsi'] = ta.momentum.rsi(df['close'])

    # 3. Bollinger Bands (볼린저 밴드)
    df['bb_high'] = ta.volatility.bollinger_hband(df['close'])
    df['bb_low'] = ta.volatility.bollinger_lband(df['close'])
    df['bb_mavg'] = ta.volatility.bollinger_mavg(df['close'])

    # 4. Stochastic Oscillator (스토캐스틱 오실레이터)
    df['stoch_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'])
    df['stoch_d'] = ta.momentum.stoch_signal(df['high'], df['low'], df['close'])

    # 지표 계산 후 NaN 값 여부 확인
    print("\n지표 계산 후 NaN 값 여부 확인:")
    print(df[['macd', 'macd_signal', 'macd_diff', 'rsi', 'bb_high', 'bb_low', 'bb_mavg', 'stoch_k', 'stoch_d']].isna().sum())

    # NaN 값이 있는 행 제거
    # df.dropna(inplace=True)

    # 지표 출력 (마지막 5개)
    print("\nMACD, RSI, Bollinger Bands, Stochastic (마지막 5개):")
    print(df[['macd', 'macd_signal', 'macd_diff', 'rsi', 'bb_high', 'bb_low', 'bb_mavg', 'stoch_k', 'stoch_d']].tail())

    pass
    return df