# TDPatcher

We have provided the source code and processed data to perform this study. 
The NiCad evaluation results is now updated, we will discuss details in the paper later! 
We also provide our in-the-wild evaluation results for further investigation as follow: 


Label|TODO-introducting commit|TODO-introduced Method::Lineno|TODO-dropped Method::Lineno
:---:|:---:|:---:|:---:
True|https://github.com/blaze/odo/commit/dd7803c1563faeee5d98f9364900a45c9aaeeb95|test\_compound\_primary\_key\_with\_single\_reference::601|test\_compound\_primary\_key\_with\_fkey::564_570
True|https://github.com/OpenMDAO/OpenMDAO/commit/a13c62482e45c949a47fd0f2d83a1d9ac342dcf1|test\_list\_discrete::1258|test\_list\_discrete\_filtered::1345_1351
True|https://github.com/OpenMDAO/OpenMDAO/commit/a13c62482e45c949a47fd0f2d83a1d9ac342dcf1|test\_list\_discrete::1258|test\_list\_discrete\_promoted::1429_1435
True|https://github.com/LuxCoreRender/BlendLuxCore/commit/eed2346f7c2cd06ddd9d104eb7957fd8455d744e|test\_glossycoating::133|test\_glossy2::106_108
True|https://github.com/LuxCoreRender/BlendLuxCore/commit/eed2346f7c2cd06ddd9d104eb7957fd8455d744e|test\_glossycoating::133|test\_glossytranslucent::119_121
True|https://github.com/oduwsdl/ipwb/commit/7450e406684d7739e82b1634533af05f11fe0820|iso8601ToDigits14::146|digits14ToRFC1123::125_128
True|https://github.com/golemhq/golem/commit/2d920b79b36ea12d89d493c406bf37f94abf5c93|\_parse\_execution\_data::142|get\_test\_case\_data::267_272
True|https://github.com/explosion/spaCy/commit/187f37073495211c422be719b16da4d2449c8844|test\_matcher\_match\_zero::76|test\_matcher\_phrase\_matcher::65_69
True|https://github.com/turicas/rows/commit/a27f499d25a037a123358b67ca2e1d5f407d9ebe|test\_export\_to\_json\_fobj::62|test\_3\_export\_to\_json\_filename::53_57
True|https://github.com/WangYihang/Webshell-Sniper/commit/a860e1baba1309882f7d1e43e7ed614613ca972c|sql\_exec::130|get\_currect\_database::49_53
True|https://github.com/WangYihang/Webshell-Sniper/commit/a860e1baba1309882f7d1e43e7ed614613ca972c|sql\_exec::130|get\_currect\_user::64_68
True|https://github.com/chipmuenk/pyfda/commit/a2b877011af7f30e14c8d99fa32f1daa8a12aef8|fx\_sim\_init::552|fx\_sim\_start::567_571
True|https://github.com/simpeg/simpeg/commit/581f1b15f137e414fc3ed628ffaf56c2f082ec23|dataObj2Deriv::216|dataObjDeriv::170_176
True|https://github.com/bcbio/bcbio-nextgen/commit/73e9c9698ba2110bacd4081d1e7eee9698d734c2|\_calculate\_mapping\_reads::184|\_combine\_coverages::167_172
True|https://github.com/pytorch/translate/commit/afbfcb7da67b7f4bf5b91c20478e0cb9011110d7|test\_compute\_scores::100|test\_reverse\_tgt\_tokens::16_19
True|https://github.com/pytorch/translate/commit/afbfcb7da67b7f4bf5b91c20478e0cb9011110d7|test\_compute\_scores::100|test\_convert\_hypos\_to\_tgt\_tokens::34_37
True|https://github.com/pytorch/translate/commit/afbfcb7da67b7f4bf5b91c20478e0cb9011110d7|test_compute_scores::100|test\_reverse\_scorer\_prepare\_inputs::68_71
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_sends ::390_394
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_bets ::485_489
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_broadcasts ::472_476
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_cancels ::537_541
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_credits ::365_369
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_balances ::378_382
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_dividends ::513_517
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_debits ::352_356
True|https://github.com/CounterpartyXCP/counterparty-lib/commit/2879218f392d58fe058482eec0fe33f8d7699e5b|get\_issuances ::461|get\_burns ::525_529
Unsure|https://github.com/cms-dev/cms/commit/77610b3801de6b8d150fcd9ca3879df584e0dcc3|evaluation\_finished::280|compilation\_finished::246_250
Unsure|https://github.com/tarmstrong/nbdiff/commit/2114667c1206a8cd2270f5805c964ef269df28d9|notebook::61|notebookjson::49_51
Unsure|https://github.com/openhatch/oh-mainline/commit/d79b23dac0b216ea823484cd72c668ada591de01|diffpatch\_progress::19|diffpatch\_info::9_11
Unsure|https://github.com/uclnlp/jack/commit/916f4fad133d61a3efd4983a3786c96924dfe565|conditional\_reader\_model::78|boe\_reader\_model::32_35
Unsure | https://github.com/CenterForOpenScience/osf.io/commit/6f6441b182dcb57dd4dc82cafa0861179a5ad869|test\_incorrect\_filtering\_field::165|test\_alternate\_filtering\_field::150_155      
 False  | https://github.com/tensorforce/tensorforce/commit/a772e5054393d49f9e6ddd9a081ee8b0c005c129 |                test\_advantage\_estimate::128                |        test\_early\_horizon\_estimate::66_71         
 False  | https://github.com/tensorforce/tensorforce/commit/a772e5054393d49f9e6ddd9a081ee8b0c005c129 |                test\_advantage\_estimate::128                |        test\_late\_horizon\_estimate::107_110        
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |                lyra\_test\_ts::87_90                
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |               rhessi\_test\_ts::93_96               
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |             noaa\_ind\_test\_ts::99_102              
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |             fermi\_gbm\_test\_ts::69_72              
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |                goes\_test\_ts::81_84                
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |                eve\_test\_ts::59_62                 
 False  | https://github.com/sunpy/sunpy/commit/3e7e5c58d2bf7e8d10da116a8db808f3189fca61 |                      esp\_test\_ts::66                       |                norh\_test\_ts::75_78                
 False  | https://github.com/google/jax/commit/edda69ef833ff5fff7515720ce28f446034cffba |                       convolve2d::70                       |                correlate2d::94_99                 





