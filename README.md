# Financial Statement Analysis Agent
用 langflow 做一個財報分析的聊天機器人，可以從網頁上提取財務數據，以進行深入的財務報表分析。

## 2024/10/08

### 資料來源
- 公開資訊觀測站 (https://mops.twse.com.tw/mops/web/t57sb01_q1)

### 目前進度
1. 手動從公開資訊觀測站下載資料後，使用 main.py 將 pdf 文件中的文字和圖片資料提取至 txt
2. 在 langflow 上將加載的文本分割，並 Embeddings 轉換成數學向量後，儲存到 Chroma DB
3. 接收用戶輸入的查詢或問題，從存儲的向量中進行查詢操作，再將 Cohere 生成的回應顯示給用戶

![image](https://github.com/user-attachments/assets/04210a99-5626-4a09-8351-ceee2725c8ec)

### 測試結果
<img width="600" alt="image" src="https://github.com/user-attachments/assets/1a1214fd-c543-4dc2-9ad9-9e95f9d4997b">

### 未來展望
1. 將 main.py 整合到 langflow 上
2. 將手動下載改成可以直接在網路上抓資料

## 2024/10/29

### 資料來源
- 台灣股市資訊網 (https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID=2330)

### 目前進度
1. 從 chat input 的問題中，用 Cohere 得到想查詢的股票代碼，並得到網頁 URL
2. 用 Firecrawl Scrape API 抓取網頁資料，並用 Custom Component: Delimited Text Extractor 擷取需要的部分

![image](https://github.com/user-attachments/assets/8f30d5ea-0bd2-4655-b78f-4582f30edf82)

### 測試結果
<img width="600" alt="image" src="https://github.com/user-attachments/assets/feb750c4-744d-479f-85ea-7d77cf38730c">


### 未來展望
1. 增加分析目標
    - 比率分析：闡釋公司關鍵財務比率及其意義
    - 趨勢分析：縱向分析公司的歷史表現
    - 橫向分析：跨時期、行業的對比
2. 優化模型
    - 修改 prompt 內容和各個參數
