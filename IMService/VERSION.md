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

# BM Version 1.1

1. Update build.gradle to version 6.6.1
2. Add 'es.predictions.inventory.path' to db.properties which indicates the path of h0,h1,h2,h3 in predictions index
3. Add new service to return daily inventory "/api/inventory/daily/count" .
4. Make Day objects immutable

# BM Version 1.7
1. Add new API to return daily impressions. The document is in doc/api-daily-count.md


