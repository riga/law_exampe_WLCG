![law](https://raw.githubusercontent.com/riga/law/master/logo.png)

# Run Jobs and Store Data on the WLCG using *luigi* and *law*


### Getting started

To get familiar with law, have a look at these simple examples:

- [loremipsum](https://github.com/riga/law/tree/master/examples/loremipsum) (measuring character frequencies)
- [lsf_at_cern](https://github.com/riga/law/tree/master/examples/lsf_at_cern) (workflows that submit tasks via LSF)


### Requirements and Setup

**Note**: The tasks in this example analysis require gfal2 and gfal2-python to be installed on your system. Both libraries should be already installed in CERN lxplus machines.

Source the minimal software stack which installs *luigi* and *law* in a local directory:

```bash
$ source setup.sh
```

TODO.


### Resources

- [law](https://github.com/riga/law)
- [luigi](http://luigi.readthedocs.io/en/stable)
- TODO


### Authors

- [Marcel R.](https://github.com/riga)


### License

The MIT License (MIT)

Copyright (c) 2018 Marcel R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
