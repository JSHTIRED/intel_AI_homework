# intel_AI_homework  
it is sub


##hw3
## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S| 0.2500| FPS: 4.70 |1.650| 16|865 |all data is '-' | 
|EfficientNet-B0| 0.8588| FPS: 7.71|0.121|16|865|NONE|
|DeiT-Tiny|  1| FPS: 5.08 |0.281|16|865|all data is '+'|
|MobileNet-V3-large-1x| 1| FPS: 6.89 |0.29 | 16|865 |NONE |


## FPS 측정 방법  
s=time.time()  
e=time.time()  
fps=1/(e-s)  
