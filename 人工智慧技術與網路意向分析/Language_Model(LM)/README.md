什麼是語言模型？
- 和時間、出現順序高度相關的模型

1.「統計式的」語言模型為一機率分佈 
- if 有一字串的長度為m，then Prob{$w_1, w_2, ..., w_m}

Tool: 
(1) N-gram
(2) Hidden Markov Model (HMM)

\
2. 基於深度學習的語言模型
(1) Transformer
(2) Bert
(3) 使用 Bert 預訓練模型

\
3. Application
(1) Transformer - 估計隱蔽字，以及機率（信心）程度
(2) 使用 pytorch建立命名實體識別器
(3) 使用 Huggingface 上的模型進行詞性標註（POS-tagging）
(4) 使用 Sentence Transformer 套件
