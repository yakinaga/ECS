@256 // 0
D=A // 1
@SP // 2
M=D // 3
// call Sys.init 0
//+++ push label_uniq_1
@label_uniq_1 // 4
D=A // 5
@SP // 6
A=M // 7
M=D // 8
@SP // 9
M=M+1 // 10
//+++ push LCL
@LCL // 11
D=M // 12
@SP // 13
A=M // 14
M=D // 15
@SP // 16
M=M+1 // 17
//+++ push ARG
@ARG // 18
D=M // 19
@SP // 20
A=M // 21
M=D // 22
@SP // 23
M=M+1 // 24
//+++ push THIS
@THIS // 25
D=M // 26
@SP // 27
A=M // 28
M=D // 29
@SP // 30
M=M+1 // 31
//+++ push THAT
@THAT // 32
D=M // 33
@SP // 34
A=M // 35
M=D // 36
@SP // 37
M=M+1 // 38
//+++ ARG = SP-0-5
@5 // 39
D=A // 40
@0 // 41
D=D+A // 42
@SP // 43
D=M-D // 44
@ARG // 45
M=D // 46
//+++ LCL=SP
@SP // 47
D=M // 48
@LCL // 49
M=D // 50
//+++ goto Sys.init
@Sys.init // 51
0;JMP // 52
//+++ (return address)
(label_uniq_1)
// function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG // 53
D=M // 54
@0 // 55
AD=D+A // 56
D=M // 57
@SP // 58
A=M // 59
M=D // 60
@SP // 61
M=M+1 // 62
// push constant 2
@2 // 63
D=A // 64
@SP // 65
A=M // 66
M=D // 67
@SP // 68
M=M+1 // 69
// lt
@SP // 70
A=M-1 // 71
D=M // 72
A=A-1 // 73
D=M-D // 74
@label_uniq_2 // 75
D;JLT // 76
@2 // 77
D=A // 78
@SP // 79
A=M-D // 80
M=0 // 81
@label_uniq_3 // 82
0;JMP // 83
(label_uniq_2)
@2 // 84
D=A // 85
@SP // 86
A=M-D // 87
M=-1 // 88
(label_uniq_3)
@SP // 89
M=M-1 // 90
// if-goto IF_TRUE
@SP // 91
A=M-1 // 92
D=M // 93
@SP // 94
M=M-1 // 95
@Main.fibonacci$IF_TRUE // 96
D;JNE // 97
// goto IF_FALSE
@Main.fibonacci$IF_FALSE // 98
0;JMP // 99
// label IF_TRUE
(Main.fibonacci$IF_TRUE)
// push argument 0
@ARG // 100
D=M // 101
@0 // 102
AD=D+A // 103
D=M // 104
@SP // 105
A=M // 106
M=D // 107
@SP // 108
M=M+1 // 109
// return
@LCL // 110
D=M // 111
@FRAME // 112
M=D // 113
@5 // 114
D=A // 115
@FRAME // 116
A=M-D // 117
D=M // 118
@RET // 119
M=D // 120
@SP // 121
A=M-1 // 122
D=M // 123
@ARG // 124
A=M // 125
M=D // 126
@ARG // 127
D=M+1 // 128
@SP // 129
M=D // 130
@FRAME // 131
AM=M-1 // 132
D=M // 133
@THAT // 134
M=D // 135
@FRAME // 136
AM=M-1 // 137
D=M // 138
@THIS // 139
M=D // 140
@FRAME // 141
AM=M-1 // 142
D=M // 143
@ARG // 144
M=D // 145
@FRAME // 146
AM=M-1 // 147
D=M // 148
@LCL // 149
M=D // 150
@RET // 151
A=M // 152
0;JMP // 153
// label IF_FALSE
(Main.fibonacci$IF_FALSE)
// push argument 0
@ARG // 154
D=M // 155
@0 // 156
AD=D+A // 157
D=M // 158
@SP // 159
A=M // 160
M=D // 161
@SP // 162
M=M+1 // 163
// push constant 2
@2 // 164
D=A // 165
@SP // 166
A=M // 167
M=D // 168
@SP // 169
M=M+1 // 170
// sub
@SP // 171
A=M-1 // 172
D=M // 173
A=A-1 // 174
M=M-D // 175
@SP // 176
M=M-1 // 177
// call Main.fibonacci 1
//+++ push label_uniq_4
@label_uniq_4 // 178
D=A // 179
@SP // 180
A=M // 181
M=D // 182
@SP // 183
M=M+1 // 184
//+++ push LCL
@LCL // 185
D=M // 186
@SP // 187
A=M // 188
M=D // 189
@SP // 190
M=M+1 // 191
//+++ push ARG
@ARG // 192
D=M // 193
@SP // 194
A=M // 195
M=D // 196
@SP // 197
M=M+1 // 198
//+++ push THIS
@THIS // 199
D=M // 200
@SP // 201
A=M // 202
M=D // 203
@SP // 204
M=M+1 // 205
//+++ push THAT
@THAT // 206
D=M // 207
@SP // 208
A=M // 209
M=D // 210
@SP // 211
M=M+1 // 212
//+++ ARG = SP-1-5
@5 // 213
D=A // 214
@1 // 215
D=D+A // 216
@SP // 217
D=M-D // 218
@ARG // 219
M=D // 220
//+++ LCL=SP
@SP // 221
D=M // 222
@LCL // 223
M=D // 224
//+++ goto Main.fibonacci
@Main.fibonacci // 225
0;JMP // 226
//+++ (return address)
(label_uniq_4)
// push argument 0
@ARG // 227
D=M // 228
@0 // 229
AD=D+A // 230
D=M // 231
@SP // 232
A=M // 233
M=D // 234
@SP // 235
M=M+1 // 236
// push constant 1
@1 // 237
D=A // 238
@SP // 239
A=M // 240
M=D // 241
@SP // 242
M=M+1 // 243
// sub
@SP // 244
A=M-1 // 245
D=M // 246
A=A-1 // 247
M=M-D // 248
@SP // 249
M=M-1 // 250
// call Main.fibonacci 1
//+++ push label_uniq_5
@label_uniq_5 // 251
D=A // 252
@SP // 253
A=M // 254
M=D // 255
@SP // 256
M=M+1 // 257
//+++ push LCL
@LCL // 258
D=M // 259
@SP // 260
A=M // 261
M=D // 262
@SP // 263
M=M+1 // 264
//+++ push ARG
@ARG // 265
D=M // 266
@SP // 267
A=M // 268
M=D // 269
@SP // 270
M=M+1 // 271
//+++ push THIS
@THIS // 272
D=M // 273
@SP // 274
A=M // 275
M=D // 276
@SP // 277
M=M+1 // 278
//+++ push THAT
@THAT // 279
D=M // 280
@SP // 281
A=M // 282
M=D // 283
@SP // 284
M=M+1 // 285
//+++ ARG = SP-1-5
@5 // 286
D=A // 287
@1 // 288
D=D+A // 289
@SP // 290
D=M-D // 291
@ARG // 292
M=D // 293
//+++ LCL=SP
@SP // 294
D=M // 295
@LCL // 296
M=D // 297
//+++ goto Main.fibonacci
@Main.fibonacci // 298
0;JMP // 299
//+++ (return address)
(label_uniq_5)
// add
@SP // 300
A=M-1 // 301
D=M // 302
A=A-1 // 303
M=D+M // 304
@SP // 305
M=M-1 // 306
// return
@LCL // 307
D=M // 308
@FRAME // 309
M=D // 310
@5 // 311
D=A // 312
@FRAME // 313
A=M-D // 314
D=M // 315
@RET // 316
M=D // 317
@SP // 318
A=M-1 // 319
D=M // 320
@ARG // 321
A=M // 322
M=D // 323
@ARG // 324
D=M+1 // 325
@SP // 326
M=D // 327
@FRAME // 328
AM=M-1 // 329
D=M // 330
@THAT // 331
M=D // 332
@FRAME // 333
AM=M-1 // 334
D=M // 335
@THIS // 336
M=D // 337
@FRAME // 338
AM=M-1 // 339
D=M // 340
@ARG // 341
M=D // 342
@FRAME // 343
AM=M-1 // 344
D=M // 345
@LCL // 346
M=D // 347
@RET // 348
A=M // 349
0;JMP // 350
// function Sys.init 0
(Sys.init)
// push constant 4
@4 // 351
D=A // 352
@SP // 353
A=M // 354
M=D // 355
@SP // 356
M=M+1 // 357
// call Main.fibonacci 1
//+++ push label_uniq_6
@label_uniq_6 // 358
D=A // 359
@SP // 360
A=M // 361
M=D // 362
@SP // 363
M=M+1 // 364
//+++ push LCL
@LCL // 365
D=M // 366
@SP // 367
A=M // 368
M=D // 369
@SP // 370
M=M+1 // 371
//+++ push ARG
@ARG // 372
D=M // 373
@SP // 374
A=M // 375
M=D // 376
@SP // 377
M=M+1 // 378
//+++ push THIS
@THIS // 379
D=M // 380
@SP // 381
A=M // 382
M=D // 383
@SP // 384
M=M+1 // 385
//+++ push THAT
@THAT // 386
D=M // 387
@SP // 388
A=M // 389
M=D // 390
@SP // 391
M=M+1 // 392
//+++ ARG = SP-1-5
@5 // 393
D=A // 394
@1 // 395
D=D+A // 396
@SP // 397
D=M-D // 398
@ARG // 399
M=D // 400
//+++ LCL=SP
@SP // 401
D=M // 402
@LCL // 403
M=D // 404
//+++ goto Main.fibonacci
@Main.fibonacci // 405
0;JMP // 406
//+++ (return address)
(label_uniq_6)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE // 407
0;JMP // 408
