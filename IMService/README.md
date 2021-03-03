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

### Requirements

1. Java 8
2. Gradle 6.6.1

### Run
This project uses gradle as a build tool.
'gradle tasks' shows different tasks that are handle by jar and war plugins.
'gradle war' to compile and build the project.
Default value for webAppDirName is src/main/webapp

### War

The default behavior of the War task is to copy the content of src/main/webapp to the root of the archive. 
Your webapp directory may of course contain a WEB-INF sub-directory, which may contain a web.xml file. 
Your compiled classes are compiled to WEB-INF/classes. 
All the dependencies of the runtime [1] configuration are copied to WEB-INF/lib.


