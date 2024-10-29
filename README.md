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

![image](https://github.com/user-attachments/assets/8443c6ee-d312-48a4-960b-ff9b453a31b1)

#### Custom Component: Delimited Text Extractor
```python
import re
from langflow.base.io.text import TextComponent
from langflow.io import MultilineInput, Output
from langflow.schema import Data


class DelimitedTextExtractor(TextComponent):
    display_name = "Delimited Text Extractor"
    description = "Extract text between specified start and end delimiters, then remove text between another set of delimiters."
    icon = "type"
    name = "DelimitedTextExtractor"
  
    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Text",
            info="Text to be processed.",
        ),
        MultilineInput(
            name="retrieve_start_delimiter",
            display_name="Retrieve Start Delimiter",
            info="The starting text delimiter for extraction.",
            value="retrieve_start",
        ),
        MultilineInput(
            name="retrieve_end_delimiter",
            display_name="Retrieve End Delimiter",
            info="The ending text delimiter for extraction.",
            value="retrieve_end",
        ),
        MultilineInput(
            name="remove_start_delimiter",
            display_name="Remove Start Delimiter",
            info="The starting text delimiter for removal.",
            value="remove_start",
        ),
        MultilineInput(
            name="remove_end_delimiter",
            display_name="Remove End Delimiter",
            info="The ending text delimiter for removal.",
            value="remove_end",
        ),
    ]
    outputs = [
        Output(display_name="Extracted Data", name="extracted_data", method="extract_data_between_delimiters"),
    ]
  
    def extract_data_between_delimiters(self) -> Data:
        start = re.escape(self.retrieve_start_delimiter)
        end = re.escape(self.retrieve_end_delimiter)
        extract_pattern = f"{start}(.*?){end}"
        
        match = re.search(extract_pattern, self.input_value, re.DOTALL)
        if match:
            extracted_text = match.group(1).strip()
        else:
            extracted_text = f"No content found between '{self.retrieve_start_delimiter}' and '{self.retrieve_end_delimiter}'."
        
        remove_start = re.escape(self.remove_start_delimiter)
        remove_end = re.escape(self.remove_end_delimiter)
        remove_pattern = f"(?<={remove_start})(.*?){remove_end}"
        modified_extracted_text = re.sub(remove_pattern, '', extracted_text, flags=re.DOTALL)
  
        modified_extracted_text = re.sub(r'\n\s*\n+', '\n', modified_extracted_text)
  
        self.status = modified_extracted_text
        return Data(data={"text": modified_extracted_text})
```

### 測試結果
<img width="600" alt="image" src="https://github.com/user-attachments/assets/feb750c4-744d-479f-85ea-7d77cf38730c">


### 未來展望
1. 增加分析目標
    - 比率分析：闡釋公司關鍵財務比率及其意義
    - 趨勢分析：縱向分析公司的歷史表現
    - 橫向分析：跨時期、行業的對比
2. 優化模型
    - 修改 prompt 內容和各個參數
