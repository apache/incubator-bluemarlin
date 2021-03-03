<!--
    Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.
-->

### Prerequisites
Gradle runs on all major operating systems and requires only a Java JDK or JRE version 8 or higher to be installed. To check, run java -version:

###  Download and Install
Download code using following git command:

git clone -b master https://github.com/Futurewei-io/blue-marlin.git

go to directory ../IMService and run gradle war to build war file.

The war file will be created in 
.../IMService/imsservice/build

Deploy the war file into a web server such as tomcat, weblogic, jboss or etc.

After starting tomcat, test the application using 
http://<server-ip>/imsservice/ping

###  Data Preparation

Three scripts are provided in .../IMService/imsservice/src/main/resources/data to generate data documents for Elasticsearch.
More information is provided by each script.

###  Testing
Run unit tests with Gradle by using the following command

$ gradle clean test
