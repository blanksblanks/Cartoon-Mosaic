![Original](_figures/sol_original.jpg)                    
![50x75](_figures/sol_mosaic_50x75.jpg)                    
![100x150](_figures/sol_mosaic_100x150.jpg)

Example output:

```
➜  Mosaic-Maker git:(master) ✗ time python main.py 512px-Statue_of_liberty_01.jpg _db/justinablakeney .png
Analyzing tile library images...
Reloaded pickled file.

Analyzing base image...
1 out of 75 rows
2 out of 75 rows
3 out of 75 rows
4 out of 75 rows
5 out of 75 rows
6 out of 75 rows
7 out of 75 rows
8 out of 75 rows
9 out of 75 rows
10 out of 75 rows
11 out of 75 rows
12 out of 75 rows
13 out of 75 rows
14 out of 75 rows
15 out of 75 rows
16 out of 75 rows
17 out of 75 rows
18 out of 75 rows
19 out of 75 rows
20 out of 75 rows
21 out of 75 rows
22 out of 75 rows
23 out of 75 rows
24 out of 75 rows
25 out of 75 rows
26 out of 75 rows
27 out of 75 rows
28 out of 75 rows
29 out of 75 rows
30 out of 75 rows
31 out of 75 rows
32 out of 75 rows
33 out of 75 rows
34 out of 75 rows
35 out of 75 rows
36 out of 75 rows
37 out of 75 rows
38 out of 75 rows
39 out of 75 rows
40 out of 75 rows
41 out of 75 rows
42 out of 75 rows
43 out of 75 rows
44 out of 75 rows
45 out of 75 rows
46 out of 75 rows
47 out of 75 rows
48 out of 75 rows
49 out of 75 rows
50 out of 75 rows
51 out of 75 rows
52 out of 75 rows
53 out of 75 rows
54 out of 75 rows
55 out of 75 rows
56 out of 75 rows
57 out of 75 rows
58 out of 75 rows
59 out of 75 rows
60 out of 75 rows
61 out of 75 rows
62 out of 75 rows
63 out of 75 rows
64 out of 75 rows
65 out of 75 rows
66 out of 75 rows
67 out of 75 rows
68 out of 75 rows
69 out of 75 rows
70 out of 75 rows
71 out of 75 rows
72 out of 75 rows
73 out of 75 rows
74 out of 75 rows
75 out of 75 rows

Generating mosaic...
1 out of 75 rows
2 out of 75 rows
3 out of 75 rows
4 out of 75 rows
5 out of 75 rows
6 out of 75 rows
7 out of 75 rows
8 out of 75 rows
9 out of 75 rows
10 out of 75 rows
11 out of 75 rows
12 out of 75 rows
13 out of 75 rows
14 out of 75 rows
15 out of 75 rows
16 out of 75 rows
17 out of 75 rows
18 out of 75 rows
19 out of 75 rows
20 out of 75 rows
21 out of 75 rows
22 out of 75 rows
23 out of 75 rows
24 out of 75 rows
25 out of 75 rows
26 out of 75 rows
27 out of 75 rows
28 out of 75 rows
29 out of 75 rows
30 out of 75 rows
31 out of 75 rows
32 out of 75 rows
33 out of 75 rows
34 out of 75 rows
35 out of 75 rows
36 out of 75 rows
37 out of 75 rows
38 out of 75 rows
39 out of 75 rows
40 out of 75 rows
41 out of 75 rows
42 out of 75 rows
43 out of 75 rows
44 out of 75 rows
45 out of 75 rows
46 out of 75 rows
47 out of 75 rows
48 out of 75 rows
49 out of 75 rows
50 out of 75 rows
51 out of 75 rows
52 out of 75 rows
53 out of 75 rows
54 out of 75 rows
55 out of 75 rows
56 out of 75 rows
57 out of 75 rows
58 out of 75 rows
59 out of 75 rows
60 out of 75 rows
61 out of 75 rows
62 out of 75 rows
63 out of 75 rows
64 out of 75 rows
65 out of 75 rows
66 out of 75 rows
67 out of 75 rows
68 out of 75 rows
69 out of 75 rows
70 out of 75 rows
71 out of 75 rows
72 out of 75 rows
73 out of 75 rows
74 out of 75 rows
75 out of 75 rows

Your 50 columns by 75 rows COLOR MOSAIC will be done soon.
Successfully saved to 512px-Statue_of_liberty_01-Mosaic1.png

Percent of possible tiles used: 25.00% (125 out 500 images from tile library used)

Expensive operations: 1308 of 3750 : 0.3488
Dominant operations: 872 of 3750 : 0.232533333333
History operations: 1570 of 3750 : 0.418666666667

python main.py 512px-Statue_of_liberty_01.jpg _db/justinablakeney .png  274.39s user 4.54s system 94% cpu 4:54.68 total
```
