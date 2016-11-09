# InfraSense 

### Contributors (Please add your name)
* Kashyap, Akash

### Setup
* Install python 3.X
* Install dependent libraries
1. pip3 install -r requirements.txt
2. (manual steps: - pip3 install Flask  
                  - pip3 install flask-cors  
                  - pip3 install flask-restful  
                  - pip3 install boto3  
                  - pip3 install peewee )
3. Setup AWS IAM user: http://docs.aws.amazon.com/lambda/latest/dg/setting-up.html#setting-up-iam                    

### Git guidelines
1. Please Fork my Repo
2. make changes 
3. please update the changes to master branch
4. Raise a PR

###NOTE: what to do before PR
 - git remote add parent https://github.com/kashypAkash/InfraSense-server.git
 - git pull parent
 - git status  # Make sure the changes are ready to be staged
 - git add .
 - git commit -m <COMMIT_NOTE>
 - git push
 
 ### Don't PR everytime :)


### Resources
AWS SDK library : https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#instance