# News / Release Notes

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
