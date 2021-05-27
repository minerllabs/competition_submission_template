# NeurIPS 2021: MineRL Competition Starter Kit

[![Discord](https://img.shields.io/discord/565639094860775436.svg)](https://discord.gg/BT9uegr)


This repository is the main MineRL 2021 Competition **submission template and starter kit**! Compete to solve obtaining diamond now!

**This repository contains**:
*  **Documentation** on how to submit your agent to the leaderboard
*  **The procedure** for Round 1 and Round 2
*  **Starter code** for you to base your submission!

**Other Resources**:
- [MineRL Competition Page](https://www.aicrowd.com/challenges/neurips-2021-minerl-competition) - Main registration page & leaderboard.
- [MineRL Documentation](http://minerl.io/docs) - Documentation for the `minerl` package and dataset!
- [Example Baselines](https://github.com/minerllabs/baselines) - A set of competition and non-competition baselines for `minerl`.


![](https://i.imgur.com/XB1WORT.gif)

#  Competition overview and tracks

The competition is centered around one goal: **obtain diamond in Minecraft** from a random starting location without any items.
There are two separate tracks with their separate rules and leaderboards. You may participate to the both or only one of them.
You need to make different submissions for the two tracks. To choose the track for a submission, see description of the `aicrowd.json` file below. 

* **Intro** track uses the `MineRLObtainDiamond-v0` environment, which provides original observation and action spaces of the environment. In this track
you are free to use any means to reach the diamond, e.g. script the agent (see the baseline solutions), or train the agent or use both! *Intro* track
only has one round (Round 1). **No training happens on the AICrowd evaluator side**, you only need to worry about the `test_submission_code.py` file.
* **Research** track uses the `MineRLObtainDiamondVectorObf-v0` environment, in which both observation and action spaces are obfuscated to prevent
manually coding actions (this is also prohibited by the rules). The amount of training is also restricted to 8M samples and four days (see rules). **Research** track has two rounds (Round 1 and 2).

#  Competition Procedure - Intro track

In the intro track you will train your agents locally and upload them to AICrowd (via git) to be evaluated by the organizers.

1. **Sign up** to join the competition [on the AIcrowd website.](https://www.aicrowd.com/challenges/neurips-2021-minerl-competition)
2. **Clone** this repo and start developing your submissions.
3. **Update** `aicrowd.json` file (team information, track information, etc. See details below).
4. **Train** your agents locally, place them under `./train` directory, update `test_submission_code.py` with your agent code and make sure the submission package works correctly with `utility/evaluation_locally.sh`.
5. [**Submit**](https://github.com/minerllabs/competition_submission_starter_template#how-to-submit-a-model) your trained models to [AIcrowd Gitlab](https://gitlab.aicrowd.com) for evaluation [(full instructions below)](#how-to-submit-a-model).  The automated evaluation setup will evaluate the submissions against the validation environment, to compute and report the metrics on the leaderboard of the competition.

After Round 1 ends, organizers will inspect the code repositories of the top participants to ensure compliance with the competition rules, after which intro track winners are announced.

#  Competition Procedure - Research track

In the Round 1 of research track you will train your agents locally with a limited number of samples and then upload them to AIcrowd (via git) to be evaluated by the organizers.

![](http://minerl.io/assets/images/round1_procedure.png)

1. **Sign up** to join the competition [on the AIcrowd website.](https://www.aicrowd.com/challenges/neurips-2021-minerl-competition)
2. **Clone** this repo  and start developing your submissions.
3. **Update** `aicrowd.json` file (team information, track information, etc. See details below).
4. **Train** your models using the `utility/train_locally.sh` script (training code **must** be inside `train_submission_code.py` file), update `test_submission_code.py` code as well and make sure the submission package works correctly with `utility/evaluation_locally.sh`.
5. [**Submit**](https://github.com/minerllabs/competition_submission_starter_template#how-to-submit-a-model) your trained models to [AIcrowd Gitlab](https://gitlab.aicrowd.com) for evaluation [(full instructions below)](#how-to-submit-a-model). The automated evaluation setup will evaluate the submissions against the validation environment, to compute and report the metrics on the leaderboard of the competition.

Note that you **must** submit your training code during Round 1 as well! Organizers use this to verify that your training follows the competition rules.

Once Round 1 is complete, the organizers will examine the code repositories of the top submissions on the leaderboard to ensure compliance with the competition rules. 

In Round 2 (Research track only), top participants of Round 1 will be invited to submit their submissions, with the evaluator system this time training the agent on the organizer's server before evaluating this. No pre-trained agents are submitted!

# How to Submit a Model!

In brief: you define your Python environment using Anaconda environment files, and AICrowd system will build a Docker image and run your code using the docker scripts inside the `utility` directory.

## Setup

1.  **Clone the github repository** or press the "Use this Template" button on GitHub!

    ```
    git clone https://github.com/minerllabs/competition_submission_starter_template.git
    ```

2. **Install** competition specific dependencies! **Make sure you have the [JDK 8 installed first](http://minerl.io/docs/tutorials/getting_started.html)!**
    ```
    # 1. Make sure to install the JDK first
    # -> Go to http://minerl.io/docs/tutorials/getting_started.html

    # 2. Install the `minerl` package and its dependencies.
    ```

3. **Specify** your specific submission dependencies (PyTorch, Tensorflow, kittens, puppies, etc.)

    * **Anaconda Environment**. To make a submission you need to specify the environment using Anaconda environment files. It is also recommended you recreate the environment on your local machine. Make sure at least version `4.5.11` is required to correctly populate `environment.yml` (By following instructions [here](https://www.anaconda.com/download)). Then:
       * **Create your new conda environment**

            ```sh
            conda env create -f environment.yml 
            conda activate minerl
            ```
      * **Your code specific dependencies**
        Add your own dependencies to the `environment.yml` file. **Remember to add any additional channels**. PyTorch requires channel `pytorch`, for example.
        You can also install them locally using
        ```sh
        conda install <your-package>
        ```

    * **Pip Packages** If you need pip packages (not on conda), you can add them to the `environment.yml` file (see the currently populated version):

    * **Apt Packages** If your training procedure or agent depends on specific Debian (Ubuntu, etc.) packages, add them to `apt.txt`.


## How do I specify my software runtime ?

As mentioned above, **the software runtime is specified mainly in 2 places**: 
* `environment.yml` -- The Anaconda environment specification. 
    If you use a conda environment to run your submission code, you can expert the exact `environment.yml` file with
    ```
    conda env export --no-build > environment.yml
    ```

* `apt.txt` -- The Debian packages (via aptitude) used by your training procedure!

These files are used to construct both the **local and AICrowd docker containers** in which your agent will train. 

If above are too restrictive for defining your environment, see [this Discourse topic for more information](https://discourse.aicrowd.com/t/how-to-specify-runtime-environment-for-your-submission/2274).

## What should my code structure be like ?

Please follow the example structure shared in the starter kit for the code structure.
The different files and directories have following meaning:

```
.
├── aicrowd.json             # Submission meta information like your username
├── apt.txt                  # Packages to be installed inside docker image
├── data                     # The downloaded data, the path to directory is also available as `MINERL_DATA_ROOT` env variable
├── test_submission_code.py  # IMPORTANT: Your testing/inference phase code. NOTE: This is NOT the the entry point for testing phase!
├── train                    # Your trained model MUST be saved inside this directory
├── train_submission_code.py # IMPORTANT: Your training phase code (only needed for the Research track)
├── test_framework.py        # The entry point for the testing phase, which sets up the environment. Your code DOES NOT go here.
└── utility                  # The utility scripts which provide a smoother experience to you.
    ├── debug_build.sh
    ├── docker_run.sh
    ├── environ.sh
    ├── evaluation_locally.sh
    ├── parser.py
    ├── train_locally.sh
    └── verify_or_download_data.sh
```

Finally, **you must specify an AIcrowd submission JSON in `aicrowd.json` to be scored!** 

The `aicrowd.json` of each submission should contain the following content:

```json
{
  "challenge_id": "aicrowd-neurips-2021-minerl-challenge",
  "grader_id": "aicrowd-neurips-2021-minerl-challenge",
  "authors": ["your-aicrowd-username"],
  "tags": "change-me",
  "description": "sample description about your awesome agent",
  "license": "MIT",
  "gpu": true
}
```

This JSON is used to map your submission to the said challenge, so please remember to use the correct `challenge_id` and `grader_id` as specified above.

Please specify if your code will use a GPU or not for the evaluation of your model. If you specify `true` for the GPU, a **NVIDIA Tesla K80 GPU** will be provided and used for the evaluation.

**Remember: You need to specify "tags" in aicrowd.json, which need to be either `"intro"` or `"research"`.** This defines the track for which you are submitting.

### Dataset location

You **don't** need to upload the MineRL dataset in submission and it will be provided in online submissions at `MINERL_DATA_ROOT` path. For local training and evaluations, you can download it once in your system via `python ./utility/verify_or_download_data.py` or place manually into `./data/` folder.


## (Research track) IMPORTANT: Saving Models during Training!

**Note: This only applies to the *Research* track**

Before you submit to the Research track, make sure that your code does the following.

* **During training** (`train_submission_code.py`) **save your models to the `train/` folder.**
* **During testing** (`test_submission_code.py`) **load your model from the `train/` folder.**

It is absolutely imperative **that you save your models during training** (`train_submission_code.py`) so that they can be used in the evaluation phase (`test_submission_code.py`) on AICrowd, and so the organizers can verify your training code in Round 1 and train agents during Round 2!

## How to submit!

To make a submission, you will have to create a private repository on [https://gitlab.aicrowd.com/](https://gitlab.aicrowd.com/).

You will have to add your SSH Keys to your GitLab account by following the instructions [here](https://docs.gitlab.com/ee/gitlab-basics/create-your-ssh-keys.html).
If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

Then you can create a submission by making a _tag push_ to your repository on [https://gitlab.aicrowd.com/](https://gitlab.aicrowd.com/).
**Any tag push (where the tag name begins with "submission-") to your private repository is considered as a submission**  
Then you can add the correct git remote, and finally submit by doing :

```
cd competition_submission_starter_template
# Add AIcrowd git remote endpoint
git remote add aicrowd git@gitlab.aicrowd.com:<YOUR_AICROWD_USER_NAME>/competition_submission_starter_template.git
git push aicrowd master

# Create a tag for your submission and push
git tag -am "submission-v0.1" submission-v0.1
git push aicrowd master
git push aicrowd submission-v0.1

# Note : If the contents of your repository (latest commit hash) does not change,
# then pushing a new tag will **not** trigger a new evaluation.
```

You now should be able to see the details of your submission at: `https://gitlab.aicrowd.com/<YOUR_AICROWD_USER_NAME>/competition_submission_starter_template/issues/`

**NOTE**: Remember to update your username in the link above :wink:

In the link above, you should start seeing something like this take shape (each of the steps can take a bit of time, so please be patient too :wink: ) :
![](https://i.imgur.com/FqScw4m.png)

and if everything works out correctly, then you should be able to see the final scores like this :
![](https://i.imgur.com/u00qcif.png)

**Best of Luck** :tada: :tada:

# Other Concepts

## (Research track) Time constraints

**Note: This only applies to the research track**.

### Round 1

You have to train your models locally **with under 8,000,000 samples** and with **worse or comprable hardware to that above** and upload the trained model in `train/` directory. But, to make sure, your training code is compatible with further round's interface, the training code will be executed in this round as well. The constraints will be a timeout of 5 minutes.

### Round 2

You are expected to train your model online using the training phase docker container and output the trained model in the `train/` directory. You need to ensure that your submission is trained in under 8,000,000 samples and within a 4 day period. Otherwise, the container will be killed

## Local evaluation

You can perform local training and evaluation using utility scripts shared in this directory. To mimic the online training phase you can run `./utility/train_locally.sh` from repository root, you can specify `--verbose` for complete logs.

```
aicrowd_minerl_starter_kit❯ ./utility/train_locally.sh --verbose
2019-07-22 07:58:38 root[77310] INFO Training Start...
2019-07-22 07:58:38 crowdai_api.events[77310] DEBUG Registering crowdAI API Event : CROWDAI_EVENT_INFO training_started {'event_type': 'minerl_challenge:training_started'} # with_oracle? : False
2019-07-22 07:58:40 minerl.env.malmo.instance.17c149[77310] INFO Starting Minecraft process: ['/var/folders/82/wsds_18s5dq321scc1j531m40000gn/T/tmpnyzpjrsc/Minecraft/launchClient.sh', '-port', '9001', '-env', '-runDir', '/var/folders/82/wsds_18s5dq321scc1j531m40000gn/T/tmpnyzpjrsc/Minecraft/run']
2019-07-22 07:58:40 minerl.env.malmo.instance.17c149[77310] INFO Starting process watcher for process 77322 @ localhost:9001
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG This mapping 'snapshot_20161220' was designed for MC 1.11! Use at your own peril.
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG #################################################
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG          ForgeGradle 2.2-SNAPSHOT-3966cea
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG   https://github.com/MinecraftForge/ForgeGradle
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG #################################################
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG                Powered by MCP unknown
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG              http://modcoderpack.com
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG          by: Searge, ProfMobius, Fesh0r,
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG          R4wk, ZeuX, IngisKahn, bspkrs
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG #################################################
2019-07-22 07:58:48 minerl.env.malmo.instance.17c149[77310] DEBUG Found AccessTransformer: malmomod_at.cfg
2019-07-22 07:58:49 minerl.env.malmo.instance.17c149[77310] DEBUG :deobfCompileDummyTask
2019-07-22 07:58:49 minerl.env.malmo.instance.17c149[77310] DEBUG :deobfProvidedDummyTask
...
```

For local evaluation of your code, you can use `./utility/evaluation_locally.sh`, add `--verbose` if you want to view complete logs.

```
aicrowd_minerl_starter_kit❯ ./utility/evaluation_locally.sh
{'state': 'RUNNING', 'score': {'score': '0.0', 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 1001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 1001, 'environment': 'MineRLObtainDiamondVectorObf-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': '0.0', 'score_secondary': 0.0}}}}
{'state': 'RUNNING', 'score': {'score': '0.0', 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 2001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 2001, 'environment': 'MineRLObtainDiamondVectorObf-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': '0.0', 'score_secondary': 0.0}}}}
{'state': 'RUNNING', 'score': {'score': '0.0', 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 3001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 3001, 'environment': 'MineRLObtainDiamondVectorObf-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': '0.0', 'score_secondary': 0.0}}}}
{'state': 'RUNNING', 'score': {'score': '0.0', 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 4001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 4001, 'environment': 'MineRLObtainDiamondVectorObf-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': '0.0', 'score_secondary': 0.0}}}}
{'state': 'RUNNING', 'score': {'score': '0.0', 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 5001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 5001, 'environment': 'MineRLObtainDiamondVectorObf-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': '0.0', 'score_secondary': 0.0}}}}
{'state': 'RUNNING', 'score': {'score': '0.0', 'score_secondary': 0.0}, 'instances': {'1': {'totalNumberSteps': 6001, 'totalNumberEpisodes': 0, 'currentEnvironment': 'MineRLObtainDiamondVectorObf-v0', 'state': 'IN_PROGRESS', 'episodes': [{'numTicks': 6001, 'environment': 'MineRLObtainDiamondVectorObf-v0', 'rewards': 0.0, 'state': 'IN_PROGRESS'}], 'score': {'score': '0.0', 'score_secondary': 0.0}}}}
...
```

For running/testing your submission in a docker environment (identical to the online submission), you can use `./utility/docker_train_locally.sh` and `./utility/docker_evaluation_locally.sh`. You can also run docker image with bash entrypoint for debugging on the go with the help of `./utility/docker_run.sh`. These scripts respect following parameters:

* `--no-build`: To skip docker image build and use the last build image
* `--nvidia`: To use `nvidia-docker` instead of `docker` which include your nvidia related drivers inside docker image


# Team

The quick-start kit was authored by 
[Anssi Kanervisto](https://github.com/Miffyli) and [Shivam Khandelwal](https://twitter.com/skbly7) with help from [William H. Guss](http://wguss.ml)

The competition is organized by the following team:

* [William H. Guss]((http://wguss.ml)) (OpenAI and Carnegie Mellon University)
* Alara Dirik (Boğaziçi University)
* Byron V. Galbraith (Talla)
* Brandon Houghton (OpenAI and Carnegie Mellon University)
* Anssi Kanervisto (University of Eastern Finland)
* Noboru Sean Kuno (Microsoft Research)
* Stephanie Milani (Carnegie Mellon University)
* Sharada Mohanty (AIcrowd)
* Karolis Ramanauskas
* Ruslan Salakhutdinov (Carnegie Mellon University)
* Rohin Shah (UC Berkeley)
* Nicholay Topin (Carnegie Mellon University)
* Steven H. Wang (UC Berkeley)
* Cody Wild (UC Berkeley)



<img src="https://d3000t1r8yrm6n.cloudfront.net/images/challenge_partners/image_file/35/CMU_wordmark_1500px-min.png" width="50%"> 

<img src="https://d3000t1r8yrm6n.cloudfront.net/images/challenge_partners/image_file/34/MSFT_logo_rgb_C-Gray.png" width="20%" style="margin-top:10px">

<img src="https://raw.githubusercontent.com/AIcrowd/AIcrowd/master/app/assets/images/misc/aicrowd-horizontal.png" width="20%"> 
