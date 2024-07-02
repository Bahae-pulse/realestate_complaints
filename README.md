# RealEstateX Complaint Management Module
**Code source for the custom module Real Estate complaint management - Bloopark Test Case 2024**
## Description

The RealEstateX Complaint Management module allows tenants to submit complaints about their rented flats through a website form. The submitted complaints are then processed and managed by RealEstateX's customer service representatives via a structured back-office pipeline.

# Features

- Public Website Form: Tenants can submit complaints without authentication.
- Automatic Assignment: Complaints are automatically assigned to customer service representatives.
- Dynamic Pipeline: Complaints move through stages: New, In Review, In Progress, Solved, Dropped.
- Work Orders: Generate printable work orders following the DIN5008 standard for required interventions.
- Email Notifications: Tenants receive emails upon complaint submission and closure.
- Comprehensive Back-office Management: Classify complaints, create action plans, and manage complaint lifecycle.

# Installation

**Prerequisites**
- Odoo 17.0
- Python(3,3.x)
- PostgreSQL 12 or above
- Docker
  
> ## Steps

**Clone the repository:**
```
git clone https://github.com/Bahae-pulse/realestate_complaints.git
```
**Navigate to the module directory:**
```
cd realestate_complaints
```
**Odoo config file (odoo.conf)**
```
[options]
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
data_dir = /var/lib/odoo/.local/share/Odoo
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
test_enable = True
test_file = realestate_complaints
dev_mode = True
```
**Dockerfile**
```
FROM odoo:17.0

USER root

# Create necessary directories and set permissions
RUN mkdir -p /var/lib/odoo/.local/share/Odoo/filestore && \
    chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo

RUN mkdir -p /var/lib/odoo/.local/share/Odoo/sessions && \
    chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo/sessions

# Install additional packages if needed
RUN pip3 install pytest

USER odoo

```
**docker-compose.yml**
```

services:
  odoo:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8070:8069"
    depends_on:
      - db
    environment:
      - POSTGRES_HOST=db:5435
      - POSTGRES_HOST=db
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_DB=postgres
      - ADDONS_PATH=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
    volumes:
      - ./extra-addons:/mnt/extra-addons
      - ./odoo.conf:/etc/odoo/odoo.conf
      - odoo-filestore:/var/lib/odoo/.local/share/Odoo/filestore
    restart: always
    networks:
      - mynetwork
    command: |
      /bin/bash -c "
      pip install pytest && \
      odoo -i realestate_complaints --dev=reload
      "

  db:
    image: postgres:latest
    environment:
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_DB=postgres
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    ports:
      - "5435:5432"
    restart: always
    networks:
      - mynetwork

volumes:
  odoo-db-data:
  odoo-filestore:

networks:
  mynetwork:
    driver: bridge

```
**Structure should be something like that:**
```
project-root/
├── extra-addons/
│   └── realestate_complaints
├── docker-compose.yml
├── Dockerfile
├── odoo.conf
└── README.md
```
**Running Docker command:**
```
docker-compose up --build -d
```
**Install the module:**
- Log in to your Odoo instance. e.g: http://localhost:8070/
- Go to Apps.
- Click on Update Apps List.
- Search for RealEstate Complaints Management and click Install or Activate.
  
<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/a35248fc-bff2-4b6d-9f2e-0e63884838bb" width="800">

#
**Configuration of Outgoing Mail Servers (Test with Gmail for exemple)**
- Go to  Settings -> Technical -> Mails -> Outgoing Mail Servers -> Add New
- Params you can use something like what i did on the screen bellow :
  
<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/b5553a4b-5362-479c-877b-a0cae8035e16" width="800">


# Usage

**Submitting a Complaint:**
- Visit the RealEstateX website under '/complaint/form' and fill out the complaint form.
  
<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/a1bb0f7e-533a-4826-a64e-19f975a698c7" width="800">

#

- Submit the form to receive a complaint success page and a confirmation email.

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/1fb54fc7-dbce-4d37-926e-20ea3ead1efa" width="800">


#
<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/65327d1d-b589-4d99-8ae3-44faf503478e" width="800">

#
**Managing Complaints:**

- Log in to the Odoo backend.
- Navigate to the Complaints menu.
- Classify, reassignment and manage complaints through the pipeline stages.
```
Sign in with an existant User ( Representative or Supervisor ) that should be as Data Demo with the Module
     ***Representative***
         login: customer_service@realestatex.com
         mdp: admin
     ***Supervisor***
         login: supervisor@realestatex.com
         mdp: admin
```
**- You'll have something like that ( without any Filter )**

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/6b2c1ea8-3d4b-4d23-a4ec-146682f32909" width="800">

#

**- You can filter with 'My complaints"  that allow to have on the view Kanban only the complaints related to the user connected**

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/6e48e77b-c28b-4d12-826e-cd7335a48b93" width="800">

#

**- Manage Complaints from the Form view ( Classify, Manage complaints regarding the type )**

*Case require intervention :*

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/535cab45-75b5-4520-bea3-b3df82c95c5d" width="800">

#
*Case Dropped complaints due to invalid content:*

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/03b289a6-7c9c-4624-8103-cd5a93d3c0cb" width="800">

#
*Case solved question complaints :*

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/5a83de3b-0b00-4a31-99eb-198c41c8c6cf" width="800">

#

**- Generating Work Orders:**

+ For complaints requiring intervention, a work order report follow the DIN5008 standard should be printed by only the supervisor from the complaint form view.

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/2fc2b35c-02b2-4a98-aa62-69e0e8cd2424" width="800">

#

+ Customer Service representative can't print report so not button available.

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/07b6cd0f-6314-47d5-94fe-eed65ac8c251" width="800">

#

+ Report looks like :

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/85f5e5b6-74d2-4603-9ce7-d6e472b86d80" width="800">

#


**- Extra configuration :**

+ We can manage the complaints stages from Complaints -> Configuration -> Complaint Stages 

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/e7fcb3bb-42ec-4cfa-8ef3-0d946d281e26" width="800">

#

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/410d00e3-2618-433d-8837-51b9a8831547" width="800">

+ We can manage the complaints tags from Complaints -> Configuration -> Complaint Tags 

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/6903569d-20b2-47ae-9ced-4ecff3bd41c7" width="800">

#

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/c0b2f742-cb30-4670-92d8-48e770c854e1" width="800">

#

**- Usefull command docker :**

+ Stop the current services:
  
```
docker-compose down
```

+ Start the services with the updated configuration:
  
```
docker-compose up -d
```

# Testing
**Unit Tests**
Unit tests are included to ensure the functionality of the module. To run the tests:
```
docker-compose exec odoo odoo -i realestate_complaints -d odoo --test-enable --stop-after-init --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
```
#

<img src="https://github.com/Bahae-pulse/realestate_complaints/assets/162335348/7c56fd70-3f0f-4246-ba0a-f8124ad8b415" width="800">

#

# Contact
For any questions or support, please contact:

Bahae: aithajjou126@gmail.com
