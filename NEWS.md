# News / Release Notes

## 2.1.2
*2025 Mar 5*
* Compatibility fixes
* Use ubuntu-24.04 runners

## 2.1.1
*2024 May 24*
* Replace instances of `docker-dev03` with `marble-dev01`

## 2.1.0
*2024 May 24*
* Upgrade supported Python versions and change installation tool from `pipenv` to `poetry`

## 2.0.0
*2021 May 19*
* Compatibility fixes
* Add new `R` handling methods

## 1.4.0
*2021 Apr 19*
* Remove `R` code from `output_handling`

## 1.3.1
*2021 Apr 14*
* Update `collect_args` to allow for multiple CSVs in one process

## 1.3.0
*2021 Apr 8*
* Add stream handling to `collect_args`

## 1.2.1
*2021 Mar 25*
* Add flexible installation scenarios for non-`R` birds

## 1.2.0
*2021 Jan 28*
* Add `ProcessError` handling methods

## 1.1.0
*2021 Jan 12*
* Add `csv_handler` to `file_handling.py`

## 1.0.3
*2021 Jan 11*
* Fix metalink call in `auto_construct_outputs`

## 1.0.2
*2021 Jan 6*

* Change`pywps>=4.2.6` and `netCDF4>=1.5.4` to resolve
compatibility and deprecation issues in birds

## 1.0.1
*2021 Jan 5*

* Fixes io bug with `url_handler` import in `io.py`

## 1.0.0
*2021 Jan 5*

* Reorganize modules into `file_handling.py`,
`logging.py`, `R.py`, `testing.py` and `io.py`
* Create `output_handling.py` module with the
functions `nc_to_dataset`, `json_to_dict`,
`rda_to_vector`, `vector_to_dict`, `txt_to_string`,
`get_robjects` and `auto_construct_outputs`

## 0.4.1
*2020 Dec 16*

* Fixes io bug with `pywps Format` import

## 0.4.0
*2020 Dec 16*

* Add `get_package`, `load_rdata_to_python` and `save_python_to_rdata` functions
* Add `rda_output` and `vector_name` outputs

## 0.3.1
*2020 Nov 26*

* Update `url_path` with new data storage location

## 0.3.0
*2020 Nov 23*

* Add `url_hanlder` and `collect_args` functions
* Add `common_status_percentages` dictionary object

## 0.2.0
*2020 Oct 28*

* Add notebook url targeting method

## 0.1.3
*2020 Sep 24*

* Add `copy_http_content` function

## 0.1.2
*2020 Aug 12*

* Add `logger` parameter to `log_handler` function

## 0.1.1
*2020 Aug 7*

* Add test suite to test `wps_tools` functions

## 0.1.0
*2020 Jul 23*

* Create wps_tools folder containing `utils.py` modules and `io_objects`
* Add `requirements.txt` and `test_requirements.txt`
* Add `python-ci` and `pypi-publish` for github actions on push
