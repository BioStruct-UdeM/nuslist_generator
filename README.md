# NUS schedule generator

## Installation

```bash
git clone https://github.com/BioStruct-UdeM/nuslist_generator.git
cd nuslist_generator
pip install -r requirements.txt
```


## Usage

```bash
usage: nuslist_generator.py [-h] --schedule_type {SB,SG,PG} --ndims {2,3,4} --density DENSITY --nx NX [--ny NY]
                            [--nz NZ]

optional arguments:
  -h, --help            show this help message and exit
  --schedule_type {SB,SG,PG}
                        schedule type: Sine-burst (SB), Sine-gap (SG), Poisson-gap (PG)
  --ndims {2,3,4}       number of dimensions: 2, 3 or 4
  --density DENSITY     density of the sampling
  --nx NX               number of points in first NUS dimension
  --ny NY               number of points in second NUS dimension
  --nz NZ               number of points in third NUS dimension
```

```bash
python nuslist_generator.py --schedule_type SB --ndims 2 --density 25 --nx 64 --ny 128
```
