# www.hopwork.fr scrapper

### System requirements

**Software**

 - OS with **python 3.5** or newer (2.7 not tested but should work)
 - virtualenv / virtualenvwrapper `[optional]`
 - **python-setuptools**
 - **python-pip**
 
**Hardware**

 - `128MB` Free RAM or more
 
 
### Used technologies

 - python-scrapy (https://scrapy.org/)
 - lxml (http://lxml.de/)
 - BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/)
 - Faker (http://faker.readthedocs.io/en/master/)
 
### Installation

Create new virtualenv at project directory, if you want:

    virtualenv .env -p /usr/bin/python3
    
then activate it, and all below commands run under this env:

    source .env/bin/activate
    
Installing requirements:

    pip3 install -r requirements.txt
    
### Running

After running scrapy spider, results would be written to `output` folder as results.csv.

    scrapy runspider hopwork/spiders/search.py
    
Storing results to file with the custom name:

    scrapy runspider hopwork/spiders/search.py -a name='another_name.csv'
     
#### Configuring search form properties

For now form is configured to get results only from `Paris`. You can easily change it by editing
json-file `filter.json`

    {
      "location": "Paris, France",
      "lon": "2.3522219000000177",
      "lat": "48.85661400000001",
      "countryCode": "FR",
      "country": "France",
      "administrativeAreaLevel1": "Île-de-France",
      "administrativeAreaLevel1Code": "Île-de-France",
      "administrativeAreaLevel2": "Paris",
      "administrativeAreaLevel2Code": "Paris",
      "administrativeAreaLevel3": "",
      "administrativeAreaLevel3Code": "",
      "administrativeAreaLevel4": "",
      "administrativeAreaLevel4Code": "",
      "city": "Paris",
      "f-fam": "",
      "f-cat": ""
    }
    
#### Add/Remove required keywords

Each keyword should be placed on a new line at `keywords.csv`.
 
    php
    ruby on rails
    symfony
    wordpress
    e-commerce
    
Each keyword will be encoded using python `urlencode` function before using it in search request. So
this keywords should looks like:

    php
    ruby+on+rails
    symfony
    wordpress
    e-commerce
    
    
### Must know

https://www.hopwork.fr disabled access to another pages if you not registered. Spider registers new user
each runtime.


Duplicate profiles are filters automatically using internal scrapy dupefilter.


Average time that needs to process all pages (for current filter.json configuration) is abocve `6 minutes`.