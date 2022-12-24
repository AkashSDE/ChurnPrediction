# **ML Model Deployment on AWS for Customer Churn Prediction**

## **Objective**

To deploy a model on AWS which predicts whether the customer is going to churn in the near future or not.

## **Tech Stack**

➔ Language: Python

➔ Libraries: Flask, gunicorn

➔ Services: Flask, Docker, AWS, Gunicorn

## **AWS Services**

-   AWS s3
-   Aws ECR
-   AWS ECS
-   AWS EC2 Load balancer
-   AWS Code commit
-   AWS Code Build
-   AWS Code Deploy
-   AWS Code Pipeline


<h2 style="text-align: center;">Step - 1</h2>
<p align="center">
<img src="media/dd6e132e02128b4e700cc944156c225e.png">
</p>


<h2 style="text-align: center;">Step - 2</h2>
<p align="center">
<img src="media/5cfaa377b2b768d36c170e45696e506e.png">
</p>

<h2 style="text-align: center;">Step - 3</h2>
<p align="center">
<img src="media/13ae9fd83f4cbb35d493b32d1a24546f.png">
</p>

1.  Create Flask Application
-  Save all the custom transformer classes – We have created transformer classes for **categorical encoding, adding features and custom scaler**. To do all the transformation of the test dataset we need to save these classes. It is saved under ML_Pipiline folder. https://github.com/AkashSDE/ChurnPrediction/tree/main/FlaskApplication/src/ML_Pipeline
-  Run engine.py https://github.com/AkashSDE/ChurnPrediction/blob/main/FlaskApplication/src/Engine.py file which will take the training dataset and train the best model with best configuration. It will the save the model in the output folder https://github.com/AkashSDE/ChurnPrediction/tree/main/FlaskApplication/output
-  Create app.py https://github.com/AkashSDE/ChurnPrediction/blob/main/FlaskApplication/src/app.py file which is the flask application with two routes /health-status and /churn-prediction. Exposed port is 5000.

<p align="center">
<img src="media/8899c3b27880f0080179ebcd9e48df9b.png">
</p>


- **predictor.py** – load the saved model, calculate the prediction, and return the results

   https://github.com/AkashSDE/ChurnPrediction/blob/main/FlaskApplication/src/predictor.py

-  Run the flask application and verify the two routes using postman.

<p align="center">
<img src="media/f72db35391db185ab633b838ae63e9e7.png">
</p>

<p align="center">
<img style="border:3px so black;" src="media/2b4d7921b74dd55517f79f00c8e82673.png"/>
</p>


    Json data

    {"data":[{"Surname": "Hargrave",

    "CreditScore": 619,

    "Geography": "France",

    "Gender": "Female",

    "Age": 42,

    "Tenure": 2,

    "Balance": 0.0,

    "NumOfProducts": 1,

    "HasCrCard": 1,

    "IsActiveMember": 1,

    "EstimatedSalary": 101348.88},

    {"Surname": "Onio",

    "CreditScore": 100,

    "Geography": "Spain",

    "Gender": "Female",

    "Age": 43,

    "Tenure": 2,

    "Balance": 1210.86,

    "NumOfProducts": 1,

    "HasCrCard": 1,

    "IsActiveMember": 1,

    "EstimatedSalary": 79084.58}

    ]

    }

2.  **Dockerize** the Flask application – Test before deploying to AWS
3.  Create the list of libraries along with the version and save it as requirement.txt\<https://github.com/AkashSDE/ChurnPrediction/blob/main/FlaskApplication/requirements.txt\>

    ![Graphical user interface, text Description automatically generated](media/c965a411d999de9c7935bff8fadd3e7c.png)

4.  Create gunicorn.sh\<https://github.com/AkashSDE/ChurnPrediction/blob/main/FlaskApplication/src/gunicorn.sh\> file to configure the flask application with WSGI sever as Flask application should not be run directly in the production server

    ![Graphical user interface, text, application Description automatically generated](media/586346d95116439935ff31addb1d815f.png)

5.  Create docker file - https://github.com/AkashSDE/ChurnPrediction/blob/main/Dockerfile

    ![Graphical user interface, text, application Description automatically generated](media/339dd096e3818edfa8904e445c34c00d.png)

6.  Build docker image and test the two routes again using postman client tool
-   Go to the folder where u kept the docker file and run the below command

    *\$ docker build -t churn-application .*

-   This will create an image churn-application check using docker images command
-   Run the below command to start the container

    *\$ Docker run -it -p 5000:5000 churn-application*

-   Go to postman client and test the two end points
1.  Create Code Commit Repo in AWS
2.  Create Code commit repository with name – **churn_prediction**

    ![Graphical user interface, text, application, email Description automatically generated](media/8499e430457f080810e04fbe1fc68b3a.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/db4c1e42208ee621ff4fa94145d8faae.png)

3.  The repository we created is a private repository. To connect with this repository, we need to create credentials.

    Go to IAM service click user select user select Security Credentials tab

    Scroll down to HTTPS Git credentials for AWS CodeCommit and click on generate credentials

    ![Graphical user interface, text, application Description automatically generated](media/ff7b51fa2ebc89afcfa880530c83ef92.png)

    Create new credentials and download the credentials – get username and password in the csv file

4.  Clone the repository in local

    Copy the HTTPS URL

    ![Graphical user interface, text, application Description automatically generated](media/dfd4b60eecaf938405cec2ef4501f7c9.png)

    In the local CLI run the below command

    \$ *git clone \<URL\>*

    it will ask for username and password which you can get from csv file which is downloaded in step b.

5.  Copy all the files and folder (exclude img folder and Readme file) from the below url to your local repository folder

    ![Graphical user interface, text, application, email Description automatically generated](media/2d602e76c611135a4bf6e98f97a48db5.png)

    [**https://github.com/AkashSDE/ChurnPrediction**](https://github.com/AkashSDE/ChurnPrediction)

6.  Do git commit and git push to the aws code repository
7.  Create testbranch and push all the changes to test branch as well

    We will use this testbranch to deploy and create pipeline

![Graphical user interface, text, application Description automatically generated](media/1740d91c22e5f2ae28c01fee550caabe.png)

1.  AWS Code build project creation
2.  Go to AWS console and search for **code build projects** click on **create build** projects

    Provide the below configuration

    ![Graphical user interface, text, application, email Description automatically generated](media/049c197a55794638987c520a8d7b5990.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/cf6eee3fb13103c626adfe675bc5dbb4.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/94962f591f90c3f2a2b998b199427fe5.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/c87caf29018fda8a56efc28c5ecf7272.png)

    ![Graphical user interface Description automatically generated with medium confidence](media/4765e98fa5b7d62ba486291d4978c1cb.png)

    ![Graphical user interface Description automatically generated with medium confidence](media/1dd667c844fdf7b0a7af9d7d325595e9.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/7294368c3652a031898c7ee5e636406d.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/5ea15ba9775b355a6e85c82bd9a753a6.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/5e3c5dcf3d2077b8edc86b7aff552e2f.png)

    Click on create build project

3.  Create buildspec.yaml file

    This yaml file contains steps to be done for building the docker image and then pushing the docker image to ecr repository

    <https://github.com/AkashSDE/ChurnPrediction/blob/main/buildspec.yaml>

![Graphical user interface, text, application, email Description automatically generated](media/89b093395d6c36441c39bd0a25bc50e3.png)

replace \<AccountId\> with your AWS account ID

1.  Create ECR repository

    ECR repository is like docker hub which is used to store the docker image built at code build stage.

    Search Elastic container repository in the aws console Click Create Repository and provide below configuration

    ![Graphical user interface, text, application, email Description automatically generated](media/7425c58d3acc06238a1f7480928590c6.png)

    ![Graphical user interface, text, application, Teams Description automatically generated](media/fc603442e2ca1ceff76d5a8ec382b76c.png)’

    Go to code build service and click on start build

    ![Graphical user interface, text, application Description automatically generated](media/ab4f48b6d920f1f6c7a2315b72957d03.png)

    Click tail logs to see the progress

    After build is successful, we can see the docker image got created inside ecr repository

    ![Graphical user interface, application Description automatically generated](media/63b7fd6bbf8559aa0df75c76c10c040d.png)

2.  ECS cluster Definition

    Search for elastic container service in aws console Click on **Clusters** in the left panel and then click on **Create Cluster** select cluster template **Networking only**  provide cluster name as **churn-cluster** and click on **create**

    ![Graphical user interface, table Description automatically generated](media/0fda4387377cedae7fa533fc1ef36c3b.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/3d6721c96ac5b1a809db4ccc8f3366ca.png)

    ![Graphical user interface, application Description automatically generated](media/333841b410339005a962d99ea211dfb3.png)

    **New cluster is created**

3.  ECS Task definition

    We need to create the task definition to run containers on the cluster that is created in the above steps.

    ![Graphical user interface, text, application Description automatically generated](media/dd55137c016c2cf3ebf3007f7868c117.png)

    ![Graphical user interface, application, Word Description automatically generated](media/560d795a785caf1987e3dd2dd3595c74.png)

    ![Graphical user interface, text, application Description automatically generated](media/7d28e4fdbf31c48a7b53e0d75b3534d5.png)

    **ecsTaskExecutionRole definition**

    ![Graphical user interface, text, application Description automatically generated](media/6601240c781135628e1ec115f52c4d6e.png)

    ![Graphical user interface, text, application, chat or text message, email Description automatically generated](media/07d9cbe5be340d4fe8de3264cfe21683.png)

    ![Graphical user interface, text, application Description automatically generated](media/f52cdc807faee633f5acdc8b0b0b81a6.png)

    **Continue task definition**

    ![Graphical user interface, text, application Description automatically generated](media/5c913ce8a8151f65113449e45f0dcd2b.png)

    Click on add container

    ![Graphical user interface, text, application Description automatically generated](media/19836c3ebaab839c7285a133fc8da64d.png)

    Leave other fields blank

    ![Graphical user interface Description automatically generated with medium confidence](media/df76711b7bb5876cfdbf0ffd07159c0a.png)

    Click on create

    ![Graphical user interface, text, application, email Description automatically generated](media/f630ce6be03d78ab599dfb6e52c1a748.png)

    New Task definition churn is created

4.  ECS service creation

    Deploy Task definition into cluster

    Create services which allow us to attach load balancer to container and we can access container client using load balancer.

    We can create as many tasks as possible which is contains a container

    First, we need to create load balancer then we can create Services in ECS

5.  Create a Load balancer
-   Create security group

    ![Graphical user interface, text, application, email Description automatically generated](media/97f17f6a549d162125eb86ed8a71a9e1.png)

    ![Graphical user interface Description automatically generated](media/73b37208ded5749f77e8ca3bf0732226.png)

    ![Graphical user interface, application Description automatically generated](media/6b4af418d25ef41fb6c6b7a3d85fa915.png)

-   Create Target groups

    ![Graphical user interface, text, application, email Description automatically generated](media/6389f1317b5a3e609ab64e8e969b1e03.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/0f8dd635ea3ded24d7110dfd322060c9.png)

    ![Graphical user interface, text, application Description automatically generated](media/e93f56584eb7791ce901360c5de6c95a.png)

    Click next and click **Create target group**

-   Create Load balancer

    Select Application Load Balancer

    ![Graphical user interface, diagram, application Description automatically generated](media/15092210568814fb12ba7a0558d597dd.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/57c4e906144a23f747b0e304bc33310e.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/99549cfb6c3157cd75c779bdc32249ff.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/80ea2d1eb259494856991b6d73e64d9e.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/1d10efb9a8cb7f6d36dff92ac7cafc1f.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/e48d0c0796467a7fdf73532b4cfeecd4.png)

    Click on Create load balancer

1.  Now go to aws console and search for ECS click on clusters

    Click on churn-cluster select Services tab click on create

    Configure service as shown in the figure below

    ![Graphical user interface, text, application Description automatically generated](media/263f920f10dbc0b7597d8dd6fef917dd.png)

    ![Graphical user interface Description automatically generated](media/a85915c8944191e67095618876a15811.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/8534a9abc44af2251f88a6fbc3f2fd80.png)

    **ecsCodeDeployRole details**

    ![Graphical user interface, text, application, email Description automatically generated](media/003fc47cf57dd465ad06af8db42dc991.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/db6e3b398e0aab0eda6f36be31b4b511.png)

    Click on **next step**

    ![Graphical user interface, text, application, email Description automatically generated](media/34e09f490e1349c1ee6d4c005efdca06.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/7c20e9bada706a6058492747fd3d3c00.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/8886b3f87cf5d229f3d670ca649eac27.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/3b7ad29aaf8355d7e372aa991557756e.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/1bb8e35a5f55dd1a97db8c4fcb84875f.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/a2bb6c3e67f3e9c12c541578b736af0e.png)

    Click on next step

    ![Graphical user interface, text, application, email Description automatically generated](media/db4e8bc0ed09fc4773f4618aca9300dd.png)

    click on next step

    Review all the details and click on create Service

    ![Graphical user interface, text, application, email Description automatically generated](media/e13a9d6cf09e8902ef34b66b16a44b74.png)

    Under Tasks Tab we can see our task definition running

    ![Graphical user interface, text, application Description automatically generated](media/ceb22aa914c68e1e13be3a4e0336c2ef.png)

    Using postman client check if the two routes are working or not – use the LB DNS name

    ![Graphical user interface, text, application, email Description automatically generated](media/d8861c6f87c43b98b2cf68ee55a4a877.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/1d06d8aee553fa555d18c7ca4110a479.png)

2.  Code deploy service

    Go to aws console search code deploy service click on applications

    Creating ecs service automatically creates an application for us in code deploy service

    ![Graphical user interface, text, application, email Description automatically generated](media/78a09e85281797d72da1cc3e28ba8f38.png)

    We can create multiple deployment groups

    ![Graphical user interface, application, Teams Description automatically generated](media/45956feac4f81680f786b67c25633d22.png)

    First, we will deploy the already created deployment group

    Click on the deployment group

    ![Graphical user interface, text, application Description automatically generated](media/19f3b28ba9926246d689fc92a6768d66.png)

    Click on create deployment

    ![Graphical user interface, application Description automatically generated](media/41635f08ecf02148a8b659c51e3f475e.png)

    Appspec editor apspec yaml we need to provide the task definition details so that aws knows where to deploy the deployment groups

    Find appspec.yaml github url

    Copy the task definition arn from the json details of task definition

    ![Graphical user interface, text, application, email Description automatically generated](media/eeea2c5029a9588b30cc642a5de464c9.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/9825451512c7fb4f5726470abb1ce46b.png)

    ![Graphical user interface, text, application Description automatically generated](media/28295ce2424004b5c05dc7f21357e5ab.png)

    ![Graphical user interface, text, application, email Description automatically generated](media/61c08a919728bfda5492ad792d3631df.png)

    Click on create deployment

    We will see the deployment status

    ![Graphical user interface, application Description automatically generated](media/43e0d1ea41e9bebd7e5f2103bd067518.png)

    ![Graphical user interface, application, table Description automatically generated](media/86b4d23df730af07c664606d12b6f62e.png)

    In the ecs task we can see the two task once the new task comes up other task will go down

    ![Graphical user interface, text, application, email Description automatically generated](media/ee36e549f1f9688f34e0a84aeedf383f.png)

    ![Graphical user interface, application Description automatically generated](media/722ec3edd32b3acd9719f469263688ac.png)

    Once the replacement is 100% ready, we can click the terminate original task set

    ![Graphical user interface, application Description automatically generated](media/a7c6a0d4fa38cb0f52f073d818f7307b.png)

3.  Code Pipeline

    Now we will create code pipeline so for every commit the code pipeline gets triggered and new version of application is deployed.

    Open code pipeline service from aws console

![Graphical user interface, text, application, email Description automatically generated](media/b1ff6de9be6e5102be53aa32ce84274f.png)

First create the taskdef.json file and commit it in the code repo

Copy the task definition details from the json tab and paste it in taskdef.json file

![Graphical user interface, text, application, email Description automatically generated](media/d73a43c9ef713be4e0f906f29f024984.png)

Replace the image name with \<IMAGE_NAME\> tag

![Graphical user interface Description automatically generated with medium confidence](media/155fc807b02e6a24c22abf7098c44761.png)

![Graphical user interface Description automatically generated with medium confidence](media/bea37f473626696109d401051fa0064b.png)

Remove the version from the task definition Arn

![Graphical user interface, text Description automatically generated](media/c391cdca3fa907f40554a89f9291923f.png)

![Graphical user interface, text, application, email Description automatically generated](media/c258a9b9a6e80e388c2b3f4608d22900.png)

Do the above changes and push the taskdef.json in the aws code repository

Click on create pipeline

![Graphical user interface, text, application, email Description automatically generated](media/44f05060121b07dd7118198e5c92e66e.png)

![Graphical user interface, text, application, email Description automatically generated](media/1648e4d897a70736f646f63b1f654a08.png)

Click next

![Graphical user interface, text, application Description automatically generated](media/26002dadaa019b200d62f1e6cf8be287.png)

![Graphical user interface, text, application, email Description automatically generated](media/ac06f5af1f56748a3e48497ad6e6e732.png)

Click next

![Graphical user interface, text, application Description automatically generated](media/8d63c69be0b8a611e18deab0875babf9.png)

![Graphical user interface, text, application Description automatically generated](media/1d1531d227362069b552ff31a73c30c6.png)

Click next

![Graphical user interface, text, application Description automatically generated](media/35603ada130a8fadc5a15db8803466a3.png)

![Graphical user interface, text, application, email Description automatically generated](media/7b4e533caa5cc0bb99934155f43496bd.png)

Click on next

![Graphical user interface, text, application, email Description automatically generated](media/76c9f618d52ac6917eeb18c795d72cb6.png)

![Graphical user interface, application, Word, Teams Description automatically generated](media/037c4382fe9fc5696dece34dfed8acd1.png)

![Background pattern Description automatically generated](media/3ae4e48249fcd37db2ef40d3698e86ae.png)

![Graphical user interface, text, application Description automatically generated](media/2d7b26f3ef1f3de9ede39abac96cbcab.png)

Click on create pipeline

It gets automatically triggered

![Graphical user interface, text, application, email Description automatically generated](media/fd3fdefa33c0b2879abf22ea28e7fa44.png)

![Graphical user interface, text, application, Teams Description automatically generated](media/124aad634d7ecb5e49121d89ae1a64d8.png)

On every commit to the code repo the pipeline gets automatically triggered and new code is deploy using blue-green deployment strategy.
