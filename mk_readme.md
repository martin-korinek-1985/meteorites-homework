# Earth Meteorite Landings Analysis homework

- Original link: https://github.com/dmachek/meteorites-homework

## Goal

Extract programmatically the list of Earth Meteorite Landings from this [dataset](https://raw.githubusercontent.com/dmachek/meteorites-homework/main/Meteorite-Landings.json)

- How many entries are in the dataset?
- What is the name and mass of the most massive meteorite in this dataset?
- What is the most frequent year in this dataset?

⚠️ **Provide your solution as a Pull Request to this repository.** ⚠️

**NOTE:** Please elaborate how did you get the results, provide the code or any means which you used to get to the results (regardless of the format/tools/framework which were used). Result itself is not sufficient.

## Solution approach

### 1) Fast prototype (mk_quick_n_dirty.py)

- First I downloaded the dataset and opened it with Total Commander Lister to glance what the data looks like.
- After that I started developing quick and dirty solution to understand more about the structure of Dataset.
- Loading file wit JSON parser failed at first, there was need to properly escape some backslashes. I encounter similar issue on another project recently. The simples solution seems to be ```input_data.replace('\\', '\\\\')```.
- With that fix I was able to load the JSON and review it in loaded debugger of Pycharm, which is very powerful and my preferred tool in such scenarios.
- With running debugger I was able to easily identify data structure and wrote simple parser to extraxt needed values (name, mass, year).
- Once I was done with seemingly working version of the script I continued to develop more robust solution.

### 2) Polished Tool (mk_extractor.py)

- At first, I tried to utilize Pandas and [Hugging Face Datasets](https://huggingface.co/docs/datasets/v1.1.1/processing.html), but I failed with both. Hugging Face Datasets is totally new to me, but I wanted to try it. With Pandas, it was not working for me, ```pd.read_json(input_file_name)``` was throwing Exception ```ValueError: Unrecognized escape sequence when decoding 'string'```, so I continued with developing of polished solution without use of Pandas.
- I added possibility to specify input attributes of the script and added proper argument parsing which is also able automatically generate help text. (See in **Example output** section)
- My general approach is that while the script is working as expected I want to output only the necessary text prints. In contrary, if something fail I want to have as much information as I can get. That is why I am printing the traceback and the exception in except clause.
- Most of my scripts (in different projects) share modul of usefully functions and proper config file, but to not overcomplicate it, I just borrow the ```debug()``` and ```log()``` functions here.
- My scripts also usually have options to ```--force-debug``` and ```--suppress-debug``` while at the same time they are autoconfigured based on which hostname they are executed on - this works fine in my scenarios, because scripts are executed from Automation Gateways which is a fix list of hostnames.

### 3) Pandas (mk_pandas.py)

- I was not satisfied with Pandas not working for me and I decide to find out how can I make it work. It turned out the issue was once again in the backslashes and by removing them and using ```pandas.DataFrame(json_data[1])``` I was able to load dataset to Pandas. Unfortunately I am not very proficient with the Pandas at the moment, so I was not able easily extract data as simply as I was able to do it with manual parsing. For that reason Pandas version is not fully developed.

## Results

- **mk_quick_n_dirty.py** is small script doing what needs to be done and can be executed without need of any additional Python Packages.
- **mk_extractor.py** is more polished version with more functionality, only dependency is on package ```pytz``` which can be removed it UTC timestamps are not needed.

### Observation

- Some meteorites do not have year.
- There is a difference with meteor and meteorite.
- Oldest meteorite in dataset is from **year 860** ("Nogoya" ID=16988).
- Lightest meteorite in the dataset has mass **only 0.01g** ("LaPaz Icefield 04531" ID=34986).
- I was not able to easily locate the source of the dataset, to find who compiled it and what data structure format is exactly used.

### Data discrepancy

I have found discrepancy about the meteorite with the most mass.

- According to provided dataset, it is:
    - ID: 11890
    - Name: **Hope**
    - Year: 1920
    - Mass: 60000000g
- But according to [kaggle](https://www.kaggle.com/datasets/nasa/meteorite-landings) it is:
    - ID: 11890
    - Name: **Hoba**
    - Year: 1920
    - Mass: 60000000g

The Gemini AI is claiming this: The most massive meteorite that fell to Earth and is still largely intact is the **Hoba** meteorite. It was discovered in 1920 on the Hoba West farm near Grootfontein, Namibia, where it remains today due to its immense size and weight (estimated to be around 60 tons).

## Used tools

- PyCharm 2025.1.2 (Community Edition)
- Total Commander 10.00

# Example output

- ```python mk_quick_n_dirty.py```

```commandline
Reading file: Meteorite-Landings.json
Parsing input data.
There are 45716 entries in the dataset.
Extracting heaviest object and year frequency.
Heaviest object is [Hope] with mass of 60,000,000 grams.
Most frequent year in dataset is 2003 with 3323 entries.
```

- ```python mk_extractor.py -h``` to print help

```commandline
usage: mk_extractor.py [-h] [--file FILE] [--debug] [--print-all | --search-id SEARCH_ID | --search-name SEARCH_NAME]

Earth Meteorite Landings Analysis

options:
  -h, --help            show this help message and exit
  --file FILE           file to parse
  --debug               force debug prints
  --print-all           print all parsed meteorites
  --search-id SEARCH_ID
                        print meteorite details by ID
  --search-name SEARCH_NAME
                        print meteorite details by name

Without specifying --print-all, --search-id or --search-name
 1) parsed meteorite count will be printed
 2) name and mass of heaviest object will be printed
 3) most frequent year in dataset will be printed
```

- ```python mk_extractor.py``` no attribute
- ```python mk_extractor.py --file=Meteorite-Landings.json``` correct JSON file specified

```commandline
1) There are 45716 entries in the dataset.
2) Heaviest object is [Hope] with mass of 60,000,000 grams.
3) Most frequent year in dataset is 2003 with 3323 entries.
```

- ```python mk_extractor.py --debug``` debug prints

```commandline
2025-06-25T12:27:50+0000 parse_known_args=Namespace(file='Meteorite-Landings.json', debug=True, print_all=False, search_id=None, search_name=None)
2025-06-25T12:27:50+0000 Reading args.file=Meteorite-Landings.json
2025-06-25T12:27:50+0000 Parsing input data.
2025-06-25T12:27:50+0000 Parsing meteorites data
1) There are 45716 entries in the dataset.
2) Heaviest object is [Hope] with mass of 60,000,000 grams.
3) Most frequent year in dataset is 2003 with 3323 entries.
```

- ```python mk_extractor.py --search-name=Hope``` search by name

```commandline
<Meteorite "Hope" Year=1920 ID=11890 Mass=60000000g>
2025-06-25T12:35:30+0000 Processing completed, meteorite found.
```

- ```python mk_extractor.py --search-id=34986``` search by ID

```commandline 
<Meteorite "LaPaz Icefield 04531" Year=2004 ID=34986 Mass=0.01g>
2025-06-25T12:37:56+0000 Processing completed, meteorite found.
```

- ```python mk_extractor.py --search-id=-1``` search by ID failed
- ```python mk_extractor.py --search-name=Hobe``` search by name failed

```commandline
WARNING Processing completed, meteorite NOT found.
```

- ```mk_extractor.py --file=mk_quick_n_dirty.py``` wrong input file

```commandline
 
Connected to pydev debugger (build 251.26094.141)
2025-06-25T12:28:44+0000 Traceback:
Traceback (most recent call last):
  File "C:\Users\markorin\PycharmProjects\homework\mk_extractor.py", line 79, in <module>
    json_data = json.loads(input_data.replace('\\', '\\\\'))
  File "C:\Users\markorin\AppData\Local\Programs\Python\Python313\Lib\json\__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "C:\Users\markorin\AppData\Local\Programs\Python\Python313\Lib\json\decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\markorin\AppData\Local\Programs\Python\Python313\Lib\json\decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

ERROR Reading data from file=mk_quick_n_dirty.py failed with Exception=Expecting value: line 1 column 1 (char 0)

Process finished with exit code 1
```

- ```python mk_pandas.py```

```commandline
Reading file: Meteorite-Landings.json
Parsing input data.
There are 45716 entries in the dataset.
```