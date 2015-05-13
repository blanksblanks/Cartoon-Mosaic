## Original image

![Original](_figures/sol_original.jpg)

Source: [http://commons.wikimedia.org/wiki/File%3AStatue_of_liberty_01.jpg](http://commons.wikimedia.org/wiki/File%3AStatue_of_liberty_01.jpg)

## Mosaic (100 columns by 150 rows)

![100x150](http://www.cs.columbia.edu/~nb2406/cs4735/images/sol_mosaic_100x150.png)

## Mosaic (50 columns by 75 rows)

![50x75](_figures/(http://www.cs.columbia.edu/~nb2406/cs4735/images/sol_mosaic_50x75.png)

Console output (note: I had to remove the .p serialization file between runs because we changed the number of desired columns so the base image object had to be recalibrated):

```
➜  Mosaic-Maker git:(master) ✗ time python main.py 512px-Statue_of_liberty_01.jpg _db/justinablakeney .png
Analyzing tile library images...
Reloaded pickled file.

Analyzing base image...
1 out of 150 rows
2 out of 150 rows
3 out of 150 rows
4 out of 150 rows
5 out of 150 rows
6 out of 150 rows
7 out of 150 rows
8 out of 150 rows
9 out of 150 rows
10 out of 150 rows
11 out of 150 rows
12 out of 150 rows
13 out of 150 rows
14 out of 150 rows
15 out of 150 rows
16 out of 150 rows
17 out of 150 rows
18 out of 150 rows
19 out of 150 rows
20 out of 150 rows
21 out of 150 rows
22 out of 150 rows
23 out of 150 rows
24 out of 150 rows
25 out of 150 rows
26 out of 150 rows
27 out of 150 rows
28 out of 150 rows
29 out of 150 rows
30 out of 150 rows
31 out of 150 rows
32 out of 150 rows
33 out of 150 rows
34 out of 150 rows
35 out of 150 rows
36 out of 150 rows
37 out of 150 rows
38 out of 150 rows
39 out of 150 rows
40 out of 150 rows
41 out of 150 rows
42 out of 150 rows
43 out of 150 rows
44 out of 150 rows
45 out of 150 rows
46 out of 150 rows
47 out of 150 rows
48 out of 150 rows
49 out of 150 rows
50 out of 150 rows
51 out of 150 rows
52 out of 150 rows
53 out of 150 rows
54 out of 150 rows
55 out of 150 rows
56 out of 150 rows
57 out of 150 rows
58 out of 150 rows
59 out of 150 rows
60 out of 150 rows
61 out of 150 rows
62 out of 150 rows
63 out of 150 rows
64 out of 150 rows
65 out of 150 rows
66 out of 150 rows
67 out of 150 rows
68 out of 150 rows
69 out of 150 rows
70 out of 150 rows
71 out of 150 rows
72 out of 150 rows
73 out of 150 rows
74 out of 150 rows
75 out of 150 rows
76 out of 150 rows
77 out of 150 rows
78 out of 150 rows
79 out of 150 rows
80 out of 150 rows
81 out of 150 rows
82 out of 150 rows
83 out of 150 rows
84 out of 150 rows
85 out of 150 rows
86 out of 150 rows
87 out of 150 rows
88 out of 150 rows
89 out of 150 rows
90 out of 150 rows
91 out of 150 rows
92 out of 150 rows
93 out of 150 rows
94 out of 150 rows
95 out of 150 rows
96 out of 150 rows
97 out of 150 rows
98 out of 150 rows
99 out of 150 rows
100 out of 150 rows
101 out of 150 rows
102 out of 150 rows
103 out of 150 rows
104 out of 150 rows
105 out of 150 rows
106 out of 150 rows
107 out of 150 rows
108 out of 150 rows
109 out of 150 rows
110 out of 150 rows
111 out of 150 rows
112 out of 150 rows
113 out of 150 rows
114 out of 150 rows
115 out of 150 rows
116 out of 150 rows
117 out of 150 rows
118 out of 150 rows
119 out of 150 rows
120 out of 150 rows
121 out of 150 rows
122 out of 150 rows
123 out of 150 rows
124 out of 150 rows
125 out of 150 rows
126 out of 150 rows
127 out of 150 rows
128 out of 150 rows
129 out of 150 rows
130 out of 150 rows
131 out of 150 rows
132 out of 150 rows
133 out of 150 rows
134 out of 150 rows
135 out of 150 rows
136 out of 150 rows
137 out of 150 rows
138 out of 150 rows
139 out of 150 rows
140 out of 150 rows
141 out of 150 rows
142 out of 150 rows
143 out of 150 rows
144 out of 150 rows
145 out of 150 rows
146 out of 150 rows
147 out of 150 rows
148 out of 150 rows
149 out of 150 rows
150 out of 150 rows

Generating mosaic...
1 out of 150 rows
2 out of 150 rows
3 out of 150 rows
4 out of 150 rows
5 out of 150 rows
6 out of 150 rows
7 out of 150 rows
8 out of 150 rows
9 out of 150 rows
10 out of 150 rows
11 out of 150 rows
12 out of 150 rows
13 out of 150 rows
14 out of 150 rows
15 out of 150 rows
16 out of 150 rows
17 out of 150 rows
18 out of 150 rows
19 out of 150 rows
20 out of 150 rows
21 out of 150 rows
22 out of 150 rows
23 out of 150 rows
24 out of 150 rows
25 out of 150 rows
26 out of 150 rows
27 out of 150 rows
28 out of 150 rows
29 out of 150 rows
30 out of 150 rows
31 out of 150 rows
32 out of 150 rows
33 out of 150 rows
34 out of 150 rows
35 out of 150 rows
36 out of 150 rows
37 out of 150 rows
38 out of 150 rows
39 out of 150 rows
40 out of 150 rows
41 out of 150 rows
42 out of 150 rows
43 out of 150 rows
44 out of 150 rows
45 out of 150 rows
46 out of 150 rows
47 out of 150 rows
48 out of 150 rows
49 out of 150 rows
50 out of 150 rows
51 out of 150 rows
52 out of 150 rows
53 out of 150 rows
54 out of 150 rows
55 out of 150 rows
56 out of 150 rows
57 out of 150 rows
58 out of 150 rows
59 out of 150 rows
60 out of 150 rows
61 out of 150 rows
62 out of 150 rows
63 out of 150 rows
64 out of 150 rows
65 out of 150 rows
66 out of 150 rows
67 out of 150 rows
68 out of 150 rows
69 out of 150 rows
70 out of 150 rows
71 out of 150 rows
72 out of 150 rows
73 out of 150 rows
74 out of 150 rows
75 out of 150 rows
76 out of 150 rows
77 out of 150 rows
78 out of 150 rows
79 out of 150 rows
80 out of 150 rows
81 out of 150 rows
82 out of 150 rows
83 out of 150 rows
84 out of 150 rows
85 out of 150 rows
86 out of 150 rows
87 out of 150 rows
88 out of 150 rows
89 out of 150 rows
90 out of 150 rows
91 out of 150 rows
92 out of 150 rows
93 out of 150 rows
94 out of 150 rows
95 out of 150 rows
96 out of 150 rows
97 out of 150 rows
98 out of 150 rows
99 out of 150 rows
100 out of 150 rows
101 out of 150 rows
102 out of 150 rows
103 out of 150 rows
104 out of 150 rows
105 out of 150 rows
106 out of 150 rows
107 out of 150 rows
108 out of 150 rows
109 out of 150 rows
110 out of 150 rows
111 out of 150 rows
112 out of 150 rows
113 out of 150 rows
114 out of 150 rows
115 out of 150 rows
116 out of 150 rows
117 out of 150 rows
118 out of 150 rows
119 out of 150 rows
120 out of 150 rows
121 out of 150 rows
122 out of 150 rows
123 out of 150 rows
124 out of 150 rows
125 out of 150 rows
126 out of 150 rows
127 out of 150 rows
128 out of 150 rows
129 out of 150 rows
130 out of 150 rows
131 out of 150 rows
132 out of 150 rows
133 out of 150 rows
134 out of 150 rows
135 out of 150 rows
136 out of 150 rows
137 out of 150 rows
138 out of 150 rows
139 out of 150 rows
140 out of 150 rows
141 out of 150 rows
142 out of 150 rows
143 out of 150 rows
144 out of 150 rows
145 out of 150 rows
146 out of 150 rows
147 out of 150 rows
148 out of 150 rows
149 out of 150 rows
150 out of 150 rows

Your 100 columns by 150 rows COLOR MOSAIC will be done soon.
Successfully saved to 512px-Statue_of_liberty_01-Mosaic1.png

Percent of possible tiles used: 42.60% (213 out 500 images from tile library used)

Expensive operations: 3768 of 15000 : 0.2512
Dominant operations: 3670 of 15000 : 0.244666666667
History operations: 7562 of 15000 : 0.504133333333
python main.py 512px-Statue_of_liberty_01.jpg _db/justinablakeney .png  887.78s user 12.58s system 96% cpu 15:37.03 total
➜  Mosaic-Maker git:(master) ✗ rm 512px-Statue_of_liberty_01.p
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
