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

### What is IMS Service?

IMS Service provided online services for Inventory Management System. These services are:

1. Impression Inventory Query: This service returns amount of inventories for a specific criteria in a period of time. The service considers existing bookings.
2. User Inventory Query: This service returns number of unique users that match specific criteria in a period of time.
3. Book Inventory: This service is to book demanded amount of impression for a specific criteria.

The IMS Service Project explains data structure for Impression Inventory, User Inventory and Book Inventory systems.
The Impression Inventory service also contains algorithms to efficiently calculate amount of inventories from raw predicted data points and booked inventories.


###  Install
Refer to doc/build-*.md for instructions on installing IMS.
