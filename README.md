# Overview

A technical interview project for data engineers.

The objective is to write a python program that will collect as many logos as you can across across a sample of websites.


# Objectives

* Write a program that will crawl a list of website and output their logo URLs.
* The program should read domain names on `STDIN` and write a CSV of domain and logo URL to `STDOUT`.
* A `websites.csv` list is included as a sample to crawl.
* You can't always get it right, but try to keep precision and recall as high as you can. Be prepared to explain ways you can improve. Bonus points if you can measure.
* Be prepared to discuss the bottlenecks as you scale up to millions of websites. You don't need to implement all the optimizations, but be able to talk about the next steps to scale it for production.
* Favicons aren't an adequate substitute for a logo, but if you choose, it's also valuable to extract as an additional field.
* Spare your time on implementing features that would be time consuming, but make a note of them so we can discuss the ideas.
* Please implement using python.
* Please keep 3rd party dependencies to a minimum, unless you feel there's an essential reason to add a dependency.
* We use [Nix](https://nixos.org/nix/) for package management. If you add your dependencies to `default.nix`, then it's easy for us to run your code. Install nix and launch the environment with `nix-shell` (works on Linux, macOS, and most unixes).

Feel free to complete as much or as little of the project as you'd like. Spare your time from implementing features that would be time consuming or uninteresting, and focus instead on parts that would make for better discussion when reviewing together. Make notes of ideas, bugs, and deficiencies to discuss together.

We recommend not using GPT, Copilot, or similar tools to generate code for this project, but if you do, please label that code clearly so we know what code you personally wrote. That code is rarely up to our standard, so we don't want it to reflect negatively on our assessment.

There's no time limit. Spend as much or as little time on it as you'd like. Clone this git repository (don't fork), and push to a new repository when you're ready to share. We'll schedule a follow-up call to review.
