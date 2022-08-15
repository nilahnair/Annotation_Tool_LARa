**Multi-Channel Time-Series Person and Soft-Biometric Identification**

This project is focused on experimenting with datasets created for Human Activity Recognition (HAR), to identify whether the individuals can be recognised irrespective of the activity being performed. In addition, the impact of activities, that were present in the dataset, on the identification accuracy was tested. Furthermore, the project attempted to make use of soft-biometrics such as age, gender, height, and weight, to create an attribute representation. This experiment was performed on LARa and PAMAP2 dataset, as these datasets have a recording protocol. 

The three datasets that were used for experimentation are:
1. [LARa](https://zenodo.org/record/3862782#.YvoQFHZByF4)
2. [OPPORTUNITY](https://archive.ics.uci.edu/ml/datasets/opportunity+activity+recognition#:~:text=Data%20Set%20Information%3A-,The%20OPPORTUNITY%20Dataset%20for%20Human%20Activity%20Recognition%20from%20Wearable%2C%20Object,%2C%20feature%20extraction%2C%20etc).)
3. [PAMAP2](https://archive.ics.uci.edu/ml/datasets/pamap2+physical+activity+monitoring)
4. [Order Picking](https://www.scitepress.org/papers/2016/58284/58284.pdf)

The networks that were used for experimentation are:
1. tCNN-IMU<sub>MLP</sub>
2. tCNN-IMU<sub>LSTM</sub>

Two types of attribute representation were created based on the recording protocol of LARa dataset. Only the subjects with IMU data were considered. 

LARa Recording Protocol:

| Subject | Gender | Age | Weight | Height | Handedness |
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

Attribute Representation:

Type 1:

| Subject | Gender |   Age   | Weight |  Height  | 
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
 
| Subject |[F/M]|A:<=30|A:30-40|A:>40|W:<=60|W:60-80|W:>80|H:<=170|H:170-180|H:>180| 
| ------- |:---:|:----:|:-----:|:---:|:----:|:-----:|:---:|:-----:|:-------:|:----:|
|    0    |  1  |  1  |  0  |  0  |  0  |   1  |  0  |  0  |   1   |  0  |
|    1    |  0  |  0  |  0  |  1  |  0  |   1  |  0  |  1  |   0   |  0  |
|    2    |  1  |  0  |  1  |  0  |  0  |   0  |  1  |  0  |   1   |  0  |
|    3    |  1  |  0  |  0  |  1  |  0  |   0  |  1  |  0  |   0   |  1  |
|    4    |  0  |  0  |  0  |  1  |  0  |   1  |  0  |  0  |   1   |  0  |
|    5    |  0  |  1  |  0  |  0  |  1  |   0  |  0  |  1  |   0   |  0  |
|    6    |  0  |  1  |  0  |  0  |  1  |   0  |  0  |  1  |   0   |  0  |
|    7    |  1  |  0  |  0  |  1  |  0  |   0  |  1  |  0  |   1   |  0  |

Where:
  A: Age
  W: Weight
  H: Height
  F: Female
  M: Male
  
PAMAP2 Recording Protocol: 

| Subject | Gender | Age | Height | Weight | Resting HR | Max HR | Dom. Hand |
| ------- |:------:|:---:|:------:|:------:|:----------:|:------:|:---------:|
|         | [F/M]  |     |  [cm]  |  [kg]  |    [bpm]   |  [bpm] |   [L/R]   |
|  101    |   M    | 27  |   182  |   83   |     75     |  193   |     R     |
|  102    |   F    | 25  |   169  |   78   |     74     |  195   |     R     | 
|  103    |   M    | 31  |   187  |   92   |     68     |  189   |     R     |
|  104    |   M    | 24  |   194  |   95   |     58     |  196   |     R     |
|  105    |   M    | 26  |   180  |   73   |     70     |  194   |     R     |
|  106    |   M    | 26  |   183  |   69   |     60     |  194   |     R     |
|  107    |   M    | 23  |   173  |   86   |     60     |  197   |     R     | 
|  108    |   M    | 32  |   179  |   87   |     66     |  188   |     L     | 
|  109    |   M    | 31  |   168  |   65   |     54     |  189   |     R     | 

Where:
 HR: Heart Rate
 Dom.: Dominant
 F: Female
 M: Male 
 L: Left
 R: Right 
 
Attribute Representation: 

| Sub |[F/M]|[L/R]|A:<=25|A:25-30|A:>30|H:<=175|H:175-185|H:>185|W:<=70|W:70-80|W:>80|
| --- |:---:|:---:|:----:|:-----:|:---:|:-----:|:-------:|:----:|:----:|:-----:|:---:|
|  0  |  1  |  1  |   0  |   1   |  0  |   0   |    1    |   0  |   0  |   0   |  1  | 
|  1  |  0  |  1  |   1  |   0   |  0  |   1   |    0    |   0  |   0  |   1   |  0  |
|  2  |  1	 |  1	 |   0	 |   0	  |  1	 |   0	  |    0	   |   1	 |   0	 |   0	  |  1  |
|  3  |  1	 |  1	 |   1	 |   0	  |  0	 |   0	  |    0	   |   1	 |   0	 |   0   | 	1  |
|  4  |  1	 |  1	 |   0	 |   1	  |  0	 |   0	  |    1    |  	0	 |   0	 |   1	  |  0  |
|  5  |  1  | 	1	 |   0	 |   1	  |  0	 |   0	  |    1	   |   0	 |   1  |  	0	  |  0  |
|  6  |  1	 |  1	 |   1  |	  0   | 	0	 |   1	  |    0	   |   0	 |   0  |  	0	  |  1  |
|  7  |  1	 |  0 	|   0	 |   0	  |  1	 |   0   |	   1	   |   0	 |   0	 |   0	  |  1  |
|  8	 |  1	 |  1	 |   0	 |   0	  |  1	 |   1	  |    0	   |   0  |	  1	 |   0	  |  0  |

Where: 
 A: Age
 H: Height
 W: Weight
 F: Female
 M: Male 
 L: Left
 R: Right 
    
It can be noticed that some individuals have the same attribute representation. For example in Type 1 attribute representation, subject 5 and 6 have the same representation, and 3 and 7 too have the same attribute representation. As a result, the representations are considered to be centers and each indiviudal is assigned to the centers based on their attribute representation, as shown in the Figure below. 
 ![](https://github.com/nilahnair/Annotation_Tool_LARa/blob/master/From_Human_Pose_to_On_Body_Devices_for_Human_Activity_Recognition/Person_SoftBio_Identification/Images/center.PNG "Attribute Representation of Individual")
 
 <p align="center">
 <img src="https://github.com/nilahnair/Annotation_Tool_LARa/blob/master/From_Human_Pose_to_On_Body_Devices_for_Human_Activity_Recognition/Person_SoftBio_Identification/Images/center.PNG">
</p>


 

