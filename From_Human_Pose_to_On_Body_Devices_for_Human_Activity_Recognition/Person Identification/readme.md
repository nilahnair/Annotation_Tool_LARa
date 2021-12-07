**Person Identification using Motion Information**

This project is focused on experimenting with datasets created for Human Activity Recognition (HAR), to identify whether the individual can be recognised irrespective of the activity being performed. In addition, the impact of activities, that were present in the dataset, on the identification accuracy was tested. Furthermore, the project attempted to make use of soft-biometrics such as age, gender, height, and weight, to create an attribute representation. 

The three datasets that are used for experimentation are:
1. LARa
2. OPPORTUNITY
3. PAMAP2

The networks that were used for experimentation are:
1. tCNN-IMU
2. deepCNNLSTM

The two types of attribute representation was created based on the recording protocol of LARa dataset. Only the subjects with IMU data were considered. 

LARa Recording Protocol:

| Subject | Sex | Age | Weight | Height | Handedness |
| ------- |:---:|:---:|:------:|:------:|:----------:|
|         |[F/M]|     |  [kg]  |  [cm]  |   [L/R]    |
|   07    |  M  |  23 |   65   |   177  |     R      |
|   08    |  F  |  51 |   68   |   168  |     R      |
|   09    |  M  |  35 |  100   |   172  |     R      |
|   10    |  M  |  49 |   97   |   181  |     R      |
|   11    |  F  |  47 |   66   |   175  |     R      |
|   12    |  F  |  23 |   48   |   163  |     R      |
|   13    |  F  |  25 |   54   |   163  |     R      |
|   14    |  M  |  54 |   90   |   177  |     R      |

Attribute Representation 

Type 1:

| Subject | Sex |   Age   | Weight |  Height  | 
| ------- |:---:|:-------:|:------:|:--------:|
|         |[F/M]|<=40/>40 |<=70/>70|<=170/>170|  
|    0    |  1  |    0    |    0   |     1    |
|    1    |  0  |    1    |    0   |     0    | 
|    2    |  1  |    0    |    1   |     1    | 
|    3    |  1  |    1    |    1   |     1    | 
|    4    |  0  |    1    |    0   |     1    | 
|    5    |  0  |    0    |    0   |     0    |  
|    6    |  0  |    0    |    0   |     0    |   
|    7    |  1  |    1    |    1   |     1    | 

Type 2:

| Subject | Sex | Age           |||  Weight        |||  Height         ||| 
|         |[F/M]| <=30|30-40| >40 | <=60| 60-80| >80 |<=170|170-180| >180|  
| ------- |:---:| ---:| ---:| ---:| ---:| ----:| ---:| ---:| -----:| ---:|
|    0    |  1  |  1  |  0  |  0  |  0  |   1  |  0  |  0  |   1   |  0  |
|    1    |  0  |  0  |  0  |  1  |  0  |   1  |  0  |  1  |   0   |  0  |
|    2    |  1  |  0  |  1  |  0  |  0  |   0  |  1  |  0  |   1   |  0  |
|    3    |  1  |  0  |  0  |  1  |  0  |   0  |  1  |  0  |   0   |  1  |
|    4    |  0  |  0  |  0  |  1  |  0  |   1  |  0  |  0  |   1   |  0  |
|    5    |  0  |  1  |  0  |  0  |  1  |   0  |  0  |  1  |   0   |  0  |
|    6    |  0  |  1  |  0  |  0  |  1  |   0  |  0  |  1  |   0   |  0  |
|    7    |  1  |  0  |  0  |  1  |  0  |   0  |  1  |  0  |   1   |  0  |






Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
