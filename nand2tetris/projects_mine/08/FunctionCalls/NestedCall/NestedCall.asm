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
// function Sys.init 0
(Sys.init)
// push constant 4000
@4000 // 53
D=A // 54
@SP // 55
A=M // 56
M=D // 57
@SP // 58
M=M+1 // 59
// pop pointer 0
@3 // 60
D=A // 61
@0 // 62
AD=D+A // 63
@R13 // 64
M=D // 65
@SP // 66
A=M-1 // 67
D=M // 68
@R13 // 69
A=M // 70
M=D // 71
@SP // 72
M=M-1 // 73
// push constant 5000
@5000 // 74
D=A // 75
@SP // 76
A=M // 77
M=D // 78
@SP // 79
M=M+1 // 80
// pop pointer 1
@3 // 81
D=A // 82
@1 // 83
AD=D+A // 84
@R13 // 85
M=D // 86
@SP // 87
A=M-1 // 88
D=M // 89
@R13 // 90
A=M // 91
M=D // 92
@SP // 93
M=M-1 // 94
// call Sys.main 0
//+++ push label_uniq_2
@label_uniq_2 // 95
D=A // 96
@SP // 97
A=M // 98
M=D // 99
@SP // 100
M=M+1 // 101
//+++ push LCL
@LCL // 102
D=M // 103
@SP // 104
A=M // 105
M=D // 106
@SP // 107
M=M+1 // 108
//+++ push ARG
@ARG // 109
D=M // 110
@SP // 111
A=M // 112
M=D // 113
@SP // 114
M=M+1 // 115
//+++ push THIS
@THIS // 116
D=M // 117
@SP // 118
A=M // 119
M=D // 120
@SP // 121
M=M+1 // 122
//+++ push THAT
@THAT // 123
D=M // 124
@SP // 125
A=M // 126
M=D // 127
@SP // 128
M=M+1 // 129
//+++ ARG = SP-0-5
@5 // 130
D=A // 131
@0 // 132
D=D+A // 133
@SP // 134
D=M-D // 135
@ARG // 136
M=D // 137
//+++ LCL=SP
@SP // 138
D=M // 139
@LCL // 140
M=D // 141
//+++ goto Sys.main
@Sys.main // 142
0;JMP // 143
//+++ (return address)
(label_uniq_2)
// pop temp 1
@5 // 144
D=A // 145
@1 // 146
AD=D+A // 147
@R13 // 148
M=D // 149
@SP // 150
A=M-1 // 151
D=M // 152
@R13 // 153
A=M // 154
M=D // 155
@SP // 156
M=M-1 // 157
// label LOOP
(Sys.init$LOOP)
// goto LOOP
@Sys.init$LOOP // 158
0;JMP // 159
// function Sys.main 5
(Sys.main)
@SP // 160
A=M // 161
M=0 // 162
@SP // 163
M=M+1 // 164
@SP // 165
A=M // 166
M=0 // 167
@SP // 168
M=M+1 // 169
@SP // 170
A=M // 171
M=0 // 172
@SP // 173
M=M+1 // 174
@SP // 175
A=M // 176
M=0 // 177
@SP // 178
M=M+1 // 179
@SP // 180
A=M // 181
M=0 // 182
@SP // 183
M=M+1 // 184
// push constant 4001
@4001 // 185
D=A // 186
@SP // 187
A=M // 188
M=D // 189
@SP // 190
M=M+1 // 191
// pop pointer 0
@3 // 192
D=A // 193
@0 // 194
AD=D+A // 195
@R13 // 196
M=D // 197
@SP // 198
A=M-1 // 199
D=M // 200
@R13 // 201
A=M // 202
M=D // 203
@SP // 204
M=M-1 // 205
// push constant 5001
@5001 // 206
D=A // 207
@SP // 208
A=M // 209
M=D // 210
@SP // 211
M=M+1 // 212
// pop pointer 1
@3 // 213
D=A // 214
@1 // 215
AD=D+A // 216
@R13 // 217
M=D // 218
@SP // 219
A=M-1 // 220
D=M // 221
@R13 // 222
A=M // 223
M=D // 224
@SP // 225
M=M-1 // 226
// push constant 200
@200 // 227
D=A // 228
@SP // 229
A=M // 230
M=D // 231
@SP // 232
M=M+1 // 233
// pop local 1
@LCL // 234
D=M // 235
@1 // 236
AD=D+A // 237
@R13 // 238
M=D // 239
@SP // 240
A=M-1 // 241
D=M // 242
@R13 // 243
A=M // 244
M=D // 245
@SP // 246
M=M-1 // 247
// push constant 40
@40 // 248
D=A // 249
@SP // 250
A=M // 251
M=D // 252
@SP // 253
M=M+1 // 254
// pop local 2
@LCL // 255
D=M // 256
@2 // 257
AD=D+A // 258
@R13 // 259
M=D // 260
@SP // 261
A=M-1 // 262
D=M // 263
@R13 // 264
A=M // 265
M=D // 266
@SP // 267
M=M-1 // 268
// push constant 6
@6 // 269
D=A // 270
@SP // 271
A=M // 272
M=D // 273
@SP // 274
M=M+1 // 275
// pop local 3
@LCL // 276
D=M // 277
@3 // 278
AD=D+A // 279
@R13 // 280
M=D // 281
@SP // 282
A=M-1 // 283
D=M // 284
@R13 // 285
A=M // 286
M=D // 287
@SP // 288
M=M-1 // 289
// push constant 123
@123 // 290
D=A // 291
@SP // 292
A=M // 293
M=D // 294
@SP // 295
M=M+1 // 296
// call Sys.add12 1
//+++ push label_uniq_3
@label_uniq_3 // 297
D=A // 298
@SP // 299
A=M // 300
M=D // 301
@SP // 302
M=M+1 // 303
//+++ push LCL
@LCL // 304
D=M // 305
@SP // 306
A=M // 307
M=D // 308
@SP // 309
M=M+1 // 310
//+++ push ARG
@ARG // 311
D=M // 312
@SP // 313
A=M // 314
M=D // 315
@SP // 316
M=M+1 // 317
//+++ push THIS
@THIS // 318
D=M // 319
@SP // 320
A=M // 321
M=D // 322
@SP // 323
M=M+1 // 324
//+++ push THAT
@THAT // 325
D=M // 326
@SP // 327
A=M // 328
M=D // 329
@SP // 330
M=M+1 // 331
//+++ ARG = SP-1-5
@5 // 332
D=A // 333
@1 // 334
D=D+A // 335
@SP // 336
D=M-D // 337
@ARG // 338
M=D // 339
//+++ LCL=SP
@SP // 340
D=M // 341
@LCL // 342
M=D // 343
//+++ goto Sys.add12
@Sys.add12 // 344
0;JMP // 345
//+++ (return address)
(label_uniq_3)
// pop temp 0
@5 // 346
D=A // 347
@0 // 348
AD=D+A // 349
@R13 // 350
M=D // 351
@SP // 352
A=M-1 // 353
D=M // 354
@R13 // 355
A=M // 356
M=D // 357
@SP // 358
M=M-1 // 359
// push local 0
@LCL // 360
D=M // 361
@0 // 362
AD=D+A // 363
D=M // 364
@SP // 365
A=M // 366
M=D // 367
@SP // 368
M=M+1 // 369
// push local 1
@LCL // 370
D=M // 371
@1 // 372
AD=D+A // 373
D=M // 374
@SP // 375
A=M // 376
M=D // 377
@SP // 378
M=M+1 // 379
// push local 2
@LCL // 380
D=M // 381
@2 // 382
AD=D+A // 383
D=M // 384
@SP // 385
A=M // 386
M=D // 387
@SP // 388
M=M+1 // 389
// push local 3
@LCL // 390
D=M // 391
@3 // 392
AD=D+A // 393
D=M // 394
@SP // 395
A=M // 396
M=D // 397
@SP // 398
M=M+1 // 399
// push local 4
@LCL // 400
D=M // 401
@4 // 402
AD=D+A // 403
D=M // 404
@SP // 405
A=M // 406
M=D // 407
@SP // 408
M=M+1 // 409
// add
@SP // 410
A=M-1 // 411
D=M // 412
A=A-1 // 413
M=D+M // 414
@SP // 415
M=M-1 // 416
// add
@SP // 417
A=M-1 // 418
D=M // 419
A=A-1 // 420
M=D+M // 421
@SP // 422
M=M-1 // 423
// add
@SP // 424
A=M-1 // 425
D=M // 426
A=A-1 // 427
M=D+M // 428
@SP // 429
M=M-1 // 430
// add
@SP // 431
A=M-1 // 432
D=M // 433
A=A-1 // 434
M=D+M // 435
@SP // 436
M=M-1 // 437
// return
@LCL // 438
D=M // 439
@FRAME // 440
M=D // 441
@5 // 442
D=A // 443
@FRAME // 444
A=M-D // 445
D=M // 446
@RET // 447
M=D // 448
@SP // 449
A=M-1 // 450
D=M // 451
@ARG // 452
A=M // 453
M=D // 454
@ARG // 455
D=M+1 // 456
@SP // 457
M=D // 458
@FRAME // 459
AM=M-1 // 460
D=M // 461
@THAT // 462
M=D // 463
@FRAME // 464
AM=M-1 // 465
D=M // 466
@THIS // 467
M=D // 468
@FRAME // 469
AM=M-1 // 470
D=M // 471
@ARG // 472
M=D // 473
@FRAME // 474
AM=M-1 // 475
D=M // 476
@LCL // 477
M=D // 478
@RET // 479
A=M // 480
0;JMP // 481
// function Sys.add12 0
(Sys.add12)
// push constant 4002
@4002 // 482
D=A // 483
@SP // 484
A=M // 485
M=D // 486
@SP // 487
M=M+1 // 488
// pop pointer 0
@3 // 489
D=A // 490
@0 // 491
AD=D+A // 492
@R13 // 493
M=D // 494
@SP // 495
A=M-1 // 496
D=M // 497
@R13 // 498
A=M // 499
M=D // 500
@SP // 501
M=M-1 // 502
// push constant 5002
@5002 // 503
D=A // 504
@SP // 505
A=M // 506
M=D // 507
@SP // 508
M=M+1 // 509
// pop pointer 1
@3 // 510
D=A // 511
@1 // 512
AD=D+A // 513
@R13 // 514
M=D // 515
@SP // 516
A=M-1 // 517
D=M // 518
@R13 // 519
A=M // 520
M=D // 521
@SP // 522
M=M-1 // 523
// push argument 0
@ARG // 524
D=M // 525
@0 // 526
AD=D+A // 527
D=M // 528
@SP // 529
A=M // 530
M=D // 531
@SP // 532
M=M+1 // 533
// push constant 12
@12 // 534
D=A // 535
@SP // 536
A=M // 537
M=D // 538
@SP // 539
M=M+1 // 540
// add
@SP // 541
A=M-1 // 542
D=M // 543
A=A-1 // 544
M=D+M // 545
@SP // 546
M=M-1 // 547
// return
@LCL // 548
D=M // 549
@FRAME // 550
M=D // 551
@5 // 552
D=A // 553
@FRAME // 554
A=M-D // 555
D=M // 556
@RET // 557
M=D // 558
@SP // 559
A=M-1 // 560
D=M // 561
@ARG // 562
A=M // 563
M=D // 564
@ARG // 565
D=M+1 // 566
@SP // 567
M=D // 568
@FRAME // 569
AM=M-1 // 570
D=M // 571
@THAT // 572
M=D // 573
@FRAME // 574
AM=M-1 // 575
D=M // 576
@THIS // 577
M=D // 578
@FRAME // 579
AM=M-1 // 580
D=M // 581
@ARG // 582
M=D // 583
@FRAME // 584
AM=M-1 // 585
D=M // 586
@LCL // 587
M=D // 588
@RET // 589
A=M // 590
0;JMP // 591