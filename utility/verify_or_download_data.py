import minerl
import minerl.data
import os

if __name__ == "__main__":
    data_dir = os.getenv('MINERL_DATA_ROOT', 'data')
    data_dir = 'data' if not data_dir else data_dir

    print("Verifying (and downloading) MineRL dataset..\n"
          "\t**If you do not want to use the data**:\n\t\t run the local evaluation scripts with `--no-data`\n"
          "\t**If you want to use your existing download of the data**:\n "
          "\t\tmake sure your MINERL_DATA_ROOT is set.\n\n")

    print("Data directory is {}".format(data_dir))
    should_download = True
    try:
        data = minerl.data.make('MineRLObtainDiamondVectorObf-v0', data_dir=data_dir)
        assert len(data._get_all_valid_recordings(data.data_dir)) > 0
        should_download = False
    except FileNotFoundError:
        print("The data directory does not exist in your submission, are you running this script from"
              " the root of the repository? data_dir={}".format(data_dir))
    except RuntimeError:
        print("The data contained in your data directory is out of date! data_dir={}".format(data_dir))
    except AssertionError:
        print("No MineRLObtainDiamond-v0 data found. Did the data really download correctly?" )

    if should_download:
        print("Attempting to download the dataset...")
        minerl.data.download(data_dir)

    print("Data verified! A+!")
