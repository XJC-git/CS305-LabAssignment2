# <center>CS305 2022 Fall Lab Assignment 2 - Raw Socket and  ICMP</center>

## Introduction

The TCP/IP protocol family can be divided into five layers: application layer, transport layer, network layer, link layer, and physical layer. 

For **standard sockets**, usually, the data is automatically encapsulated according to the selected transport layer protocol (such as TCP, or UDP).

The **raw socket** is a type of socket that allows access to the underlying transport provider, which means the raw socket allows the direct sending/receiving of IP protocol packets **without** any transport layer protocol format.

Internet Control Message Protocol(**ICMP**) is a supporting protocol in the TCP/IP protocol family. It is used by network devices, including routers, to send error messages and operational information indicating success or failure when communicating with another IP address. For details, you can refer to [RFC 792: INTERNET CONTROL MESSAGE PROTOCOL](https://www.rfc-editor.org/rfc/rfc792).

In this assignment, you need to finish all the following tasks using the **raw socket**.

## Tasks

### Task 1 Checksum (20 points (10 points for generation and 10 points for check))

The checksum is used to verify the integrity of packets, and it is carried in the header of an IP packet. Please note that there are not only checksums in IP packets, but also checksums in ICMP, UDP, and TCP packets. They correspond to the verification information of different packets or packet headers, please pay attention to distinguish them.

In this task, we hope you can implement the checksum mechanism of the ICMP packets. For how to compute the checksum of a packet, you can refer to [RFC 1071](https://www.rfc-editor.org/rfc/rfc1071).

We have provided a simple ICMP class in `sockets.py`. You need to complete the code in method `_checksum(self, data)` and `_check_data(self, data, checksum)`of the file, the  `_checksum(self, data)` method is to generate the checksum while the `_check_data(self, data, checksum)` method is to verify the integrity of the given data.

:bulb: Hint: Please pay attention to that, one importance to test in this task is the **correctness** of the calculation of the checksum. 

:exclamation:Apart from that, we believe that the smart students of SUSTech must have noticed that the basic unit for checksum is 2 bytes, so if you encounter a message with an odd length, you need to fill in the necessary padding (filling position) to meet the requirement of the calculation of the checksum.

### Task 2 ICMP Request Message (20 points)

In this task, we hope that you can correctly construct an ICMP request message according to an id, a sequence number, and a payload. The type of the ICMP request message is 8 and the code is 0. 

The only method you need to complete is ` _create_packet(self, request: ICMPRequest)` in `sockets.py`.

:star: Hint: Based on Task 1, the request message created should contain a correct checksum and the requested payload.

### Task 3 ICMP Reply Message (20 points)

In this task, we hope you can parse an ICMP reply message correctly.

The **only** method you need to complete is `_parse_reply(self, packet, source, current_time)` in `sockets.py`.

:dart: Hint: The key point of this task lies in that, you should extract and parse the id, sequence, type, code, etc. of certain ICMP packets. 

In normal cases, the ICMP Echo Message of  Echo Reply Message is shown below. The Type is equal to 8 for an echo message and 0 for an echo reply message.

![echo.png](https://s2.loli.net/2022/12/04/WlF4qL9DvmKj5uY.png)

What's more, there will be some message that appears in some abnormal response, called the **ICMP error message**. Take `Time Exceeded Message` for an example, its structure is shown below.

![error.png](https://s2.loli.net/2022/12/04/OMRvnXzVpoJLrch.png)

In the error message, the type is not equal to 0(In this Time Exceeded Message, the type is equal to 11), and the structure is different from the normal ICMP message, so you may treat them especially to parse their **type,** and **code**, and at the meantime, read the id and sequence of the original data datagram.

When receiving a message, you should first check the checksum, if the check fails, then you should report the error and terminate the analysis, if the check succeeds, congratulations, then you can start parsing it.

### Task 4 Ping (20 points)

Ping is a utility used to test the reachability of a host on an IP network, and we have learned that `ping` operates using ICMP packets. Pinging involves sending an **ICMP echo request** to the target host and waiting for an **ICMP echo reply**.

In this task, we hope that you can implement the procedure of sending a testing message under the `ping` command, including waiting for the ICMP echo reply, parsing the reply message, and printing the statics. You only need to complete the `ping(address, n=4, payload=None,id=None)` in the `ping.py`.

:shamrock: Hint: During the ping process, you need to be able to customize the **number**, **payload**, and **id** of the sent packets. Since the purpose of ping is to test the reachability of a host on an IP network, accurate calculation of **RTT** and **packet loss rate** from received packets is also one of the factors considered in the test.

After successfully implementing the ping method, use `python ping.py www.baidu.com` to run ping.py, here is an example of testing the connectivity of the Baidu website, you will get an output similar to this, as shown below.

![ping.png](https://s2.loli.net/2022/12/04/EvPK4iXG9QLWNz2.png)

In the output message, the **sent packet** is the number of packets transmitted to the destination host. The **received packet** is the number of ICMP responses received from the remote host. **Packet loss** refers to the proportion of the package that cannot reach the endpoint of the sent packages. The **Round-trip times** here are the minimum, average, and maximum of the RTT calculated in ping. The **jitter** in milliseconds is defined as the variance of the latency of packets flowing through the network.

After you have completed this method, you can customize the payload by running `python ping.py www.baidu.com -—p 'hello world'`, the result is as below.

![Screen Shot 2022-12-04 at 18.17.55](/Users/leo/Library/Application Support/typora-user-images/Screen Shot 2022-12-04 at 18.17.55.png)

### Task 5 Tracert (20 points)

Apart from `ping`, the `tracert` will also make use of the ICMP packets. The main purpose of `tracert` is to detect the routers from the source to the destination, and the distance of these routers from the source

In this task, we hope that you can implement the procedure of sending a testing message under the `tracert` command. You only need to complete the `tracert(address, id=None)` in the `tracert.py`.

:star2: Hint: In the process of tracert, we hope that you can customize the id of the sent message, and stop the cycle of sending the message when the message has reached the destination host. In this process, you should also combine the principle of tracert to appropriately change the **value of TTL**. In addition, the most important thing is that you should analyze the address of each hop from the received message, and finally, find the corresponding quest information and accurately calculate the **RTT value**.

After successfully implementing the `tracert` method, use ` python tracert.py jp.nuxjc.com` to run `tracert.py`, here is an example of testing the connectivity of the Baidu website, you will get an output similar to this, as shown below.

<img src="https://s2.loli.net/2022/12/04/aSskjRcFOHY5q8W.png" alt="tracert1.png" style="zoom:33%;" />
...

<img src="https://s2.loli.net/2022/12/04/8aGyLUPh3A1MjEk.png" alt="tracert2.png" style="zoom: 33%;" />

The number following `#` represents the index of hop and the IP address following it is the router's IP and the last one is the destination's IP. Please notice that the IP is **not required** in this assignment, it is shown just for illustrating the `tracert` process. The meaning of the corresponding field is the same as `ping`.

:chicken:ps. If you are testing `tracert.py` separately under **windows**, if you encounter information that can only display **the last hop**, it may be caused by the firewall rules in windows, please follow the steps below to set it up separately.

1. Create a new inbound rule in the advanced firewall settings

![pic1.png](https://s2.loli.net/2022/12/05/JbicPdfg9SUlpuC.png)

2. Next select "Custom"

![pic2.png](https://s2.loli.net/2022/12/05/wSLbZhrmXxYHWKs.png)

3. select "all the programs"

![pic3.png](https://s2.loli.net/2022/12/05/fZKCVTNs98ieljE.png)

4. select the "icmpv4" protocol

![pic4.png](https://s2.loli.net/2022/12/05/8Row53azlYhr4fp.png)

5. Accept all the ICMP message types.

![pic5.png](https://s2.loli.net/2022/12/05/Iz96SxDkPNCYXHc.png)

## How to run the code

### Pycharm

Move to the root directory of the assignment, and directly click the `run` button is OK.

### VScode

1. Move to the root directory of the assignment
2. Run `python -m unittest tests.ping_test` to execute the `ping_test.py`, and the execution of `tracert.py` is similar.

## Score Environment

Python 3.9

## What to submit

You must provide **a zip file** of your implementation, which contains all the code you write, which includes `ping.py`, `sockets.py`,  `tracert.py`, etc, and other files if needed.

And, the zip file should be named "SID1_SID2_SID3_labA2.zip"**, for example, "11810000_11910000_12010000_labA2.zip".

**No need for the report**, just show us your code is okay.

## Q&A Link

If you have any questions about this assignment, please go to the link below to raise your question. And we will check and reply in time.
https://github.com/XJC-git/CS305-LabAssignment2

Pay attention that the deadline for this assignment is<b style = "color:red" >  :warning:26, Dec 2022 </b >

Enjoy yourselves :basketball: