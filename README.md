# ZoKratesBenchmarks
Contains ZoKrates Benchmark scripts, related code and documentation

## Benchmarking ZoKrates Remotely 
Subsequently, we explain how to benchmark ZoKrates on a remote server to which we have `ssh` access

Assumptions for now:
- Git, Jupyter Notebook are installed
- The description below is written for a specific ISE Linux Server. Adjust commands for other machines.

TODO: remove zokrates_unoptimized binary, as this is a mac-os executable for now and we want this to be more flexible.

### Start Jupyter Notebook
1. Connect to TU VPN
2. Connect to server
    ```shell
    ssh je@kbl.ise.tu-berlin.de
    ```
3. Start Benchmarking Jupyter Notebook so that it doesn't quit when ssh session ends
    ```shell
    cd ~/ZoKratesBenchmarks
    nohup jupyter-notebook --ip=kabylake.ise.tu-berlin.de --no-browser &
    ```
4. Copy the login `token` that is printed to the console as URL querystring for the notebook. Example output:
    ```
    http://kabylake.ise.tu-berlin.de:8888/?token=a1897d2f34b3db7e4c0b82fed5ee65552dad3ccff4b89793
    ```

### Setup SSH-Tunnel for Jupyter Notebook
0. While connect to TU VPN
1. In a new terminal window, setup SSH Tunnel
    ```shell
    ssh -N -p 22 je@kbl.ise.tu-berlin.de -L 127.0.0.1:8889:kbl.ise.tu-berlin.de:8888
    ```
2. Open Browser on localhost and access remote Juypter Notebook at:

    http://localhost:8889

### Run Benchmarks
Use Jupyter Notebook UI

### Retrieve Results
 Copy results from remote server to localhost:
 ```shell
     scp -r je@kbl.ise.tu-berlin.de:~/ZoKratesBenchmarks/exports
    ~/Desktop/ZoKratesRemoteBenchmark/exports
```

## Benchmarking Setup

0. Make sure you're in the home directory
    ```shell
    cd ~/
    ```

1. Install ZoKrates 
    ```shell
    curl -LSfs get.zokrat.es | sh
    ```

2. Set environment variables in ~/.bashrc
    ```
    export PATH=$PATH:$HOME/.zokrates/bin
    export ZOKRATES_HOME=$HOME/.zokrates/stdlib
    ```

3. Update stdlib to contain mimc (PR not merged yet)
    ```shell
    git clone https://github.com/petscheit/ZoKrates.git
    cd ZoKrates
    git checkout mimc_sponge
    ```
    and then move `stlib` to the right place
    ```shell
    cp -r zokrates_stdlib/stdlib/ ~/.zokrates/stdlib/
    ```

4. Setup Benchmarking Juypter Notebook

    - Clone directly from Github (when it becomes public)
     ```shell
    cd ~/
    git clone https://github.com/JacobEberhardt/ZoKratesBenchmarks.git
    ```
    - Clone locally and copy from localhost to remote
    ```shell
    scp -r ZoKratesBenchmarks/ je@kbl.ise.tu-berlin.de:~/ZoKratesBenchmarks
    ```
5. Install Rust nightly through rustup:
    ```shell
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```
    and add nightly toolchain:
    ```shell
    rustup toolchain install nightly
    ```
    Then, make it default:
    ```shell
    rustup default nightly
    ```
    
6. Build unoptimized ZoKrates
    1. Clone branch from github
        ```shell
        cd ~/
        git clone -b benchmarks/unoptimized https://github.com/Zokrates/ZoKrates.git ZoKratesUnoptimized
        cargo +nightly build --release
        ```
    2. Build release version with nightly rust
        ```shell
        cd ~/ZoKratesUnoptimized
        cargo +nightly build --release
        ```
    3. Copy executable to user bin directory. 
        ```shell
        cp ~/ZoKratesUnoptimized/target/release/zokrates ~/bin/zokrates_unoptimized
        ```
        Make sure it's in path by adding to `~/.bashrc`
        ```
        export PATH=$PATH:$HOME/bin
        ```

7. Install stable version of the Go Ethereum client `geth`:
    ```
    sudo add-apt-repository -y ppa:ethereum/ethereum
    sudo apt-get update
    sudo apt-get install ethereum
    ```

8. Install stable version of the Solidity Compiler `solc`:
    ```
    npm i -g solc
    ```