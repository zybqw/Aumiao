
const UA: string[] = (
    `Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_3_4; en-US) AppleWebKit/600.40 (KHTML, like Gecko) Chrome/53.0.1478.400 Safari/602
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/600.17 (KHTML, like Gecko) Chrome/55.0.3366.304 Safari/602
Mozilla/5.0 (Windows; U; Windows NT 10.3; Win64; x64; en-US) AppleWebKit/602.16 (KHTML, like Gecko) Chrome/48.0.2384.263 Safari/601
Mozilla/5.0 (Windows; Windows NT 10.0; x64; en-US) AppleWebKit/535.35 (KHTML, like Gecko) Chrome/48.0.2748.138 Safari/537
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5; en-US) AppleWebKit/534.32 (KHTML, like Gecko) Chrome/51.0.2818.378 Safari/537
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_9_7) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/47.0.1738.221 Safari/534
Mozilla/5.0 (Windows; Windows NT 10.5; x64) AppleWebKit/535.10 (KHTML, like Gecko) Chrome/54.0.3879.162 Safari/534
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_3_3; en-US) AppleWebKit/533.21 (KHTML, like Gecko) Chrome/47.0.3286.253 Safari/601
Mozilla/5.0 (Linux; Linux i666 ) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/48.0.1924.370 Safari/534
Mozilla/5.0 (Linux; U; Linux x86_64) AppleWebKit/600.31 (KHTML, like Gecko) Chrome/48.0.2986.261 Safari/536
Mozilla/5.0 (Windows; U; Windows NT 6.1; WOW64) AppleWebKit/535.4 (KHTML, like Gecko) Chrome/48.0.1704.206 Safari/535
Mozilla/5.0 (U; Linux i572 x86_64) AppleWebKit/536.23 (KHTML, like Gecko) Chrome/48.0.1271.368 Safari/533
Mozilla/5.0 (Linux x86_64) AppleWebKit/533.17 (KHTML, like Gecko) Chrome/49.0.1212.313 Safari/601
Mozilla/5.0 (Windows; Windows NT 10.3; Win64; x64; en-US) AppleWebKit/534.47 (KHTML, like Gecko) Chrome/53.0.3763.301 Safari/536
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_1_7) AppleWebKit/534.49 (KHTML, like Gecko) Chrome/53.0.3752.286 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 9_3_7) AppleWebKit/601.43 (KHTML, like Gecko) Chrome/47.0.3233.115 Safari/534
Mozilla/5.0 (Linux i651 ; en-US) AppleWebKit/603.45 (KHTML, like Gecko) Chrome/53.0.1870.196 Safari/600
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_2_9; en-US) AppleWebKit/603.49 (KHTML, like Gecko) Chrome/51.0.3312.234 Safari/537
Mozilla/5.0 (U; Linux x86_64) AppleWebKit/603.15 (KHTML, like Gecko) Chrome/48.0.2280.339 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_9_8) AppleWebKit/533.19 (KHTML, like Gecko) Chrome/53.0.1208.151 Safari/601
Mozilla/5.0 (Windows; Windows NT 10.5; WOW64; en-US) AppleWebKit/533.42 (KHTML, like Gecko) Chrome/49.0.3287.158 Safari/603
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/534.35 (KHTML, like Gecko) Chrome/47.0.2224.239 Safari/534
Mozilla/5.0 (Windows; U; Windows NT 10.2; x64; en-US) AppleWebKit/600.40 (KHTML, like Gecko) Chrome/54.0.3446.282 Safari/537
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_3_9; en-US) AppleWebKit/601.32 (KHTML, like Gecko) Chrome/50.0.3100.145 Safari/534
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_8_2; en-US) AppleWebKit/602.19 (KHTML, like Gecko) Chrome/47.0.2041.201 Safari/533
Mozilla/5.0 (Windows; Windows NT 10.4; x64) AppleWebKit/533.33 (KHTML, like Gecko) Chrome/54.0.3869.298 Safari/600
Mozilla/5.0 (Windows; U; Windows NT 10.2; Win64; x64; en-US) AppleWebKit/600.28 (KHTML, like Gecko) Chrome/54.0.2625.386 Safari/602
Mozilla/5.0 (Linux; Linux x86_64; en-US) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/54.0.1434.113 Safari/537
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_3_8; en-US) AppleWebKit/603.22 (KHTML, like Gecko) Chrome/50.0.3273.119 Safari/535
Mozilla/5.0 (Linux x86_64) AppleWebKit/603.7 (KHTML, like Gecko) Chrome/51.0.1564.228 Safari/537
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4_1; en-US) AppleWebKit/603.27 (KHTML, like Gecko) Chrome/53.0.2350.114 Safari/600
Mozilla/5.0 (Windows; U; Windows NT 6.2; Win64; x64; en-US) AppleWebKit/536.23 (KHTML, like Gecko) Chrome/52.0.2213.253 Safari/533
Mozilla/5.0 (Windows; U; Windows NT 10.1;) AppleWebKit/601.8 (KHTML, like Gecko) Chrome/54.0.3469.247 Safari/600
Mozilla/5.0 (Macintosh; Intel Mac OS X 7_8_5; en-US) AppleWebKit/535.18 (KHTML, like Gecko) Chrome/47.0.1022.118 Safari/603
Mozilla/5.0 (Macintosh; Intel Mac OS X 9_8_4) AppleWebKit/537.38 (KHTML, like Gecko) Chrome/48.0.1421.298 Safari/601
Mozilla/5.0 (Windows NT 6.2;; en-US) AppleWebKit/537.27 (KHTML, like Gecko) Chrome/48.0.3539.243 Safari/536
Mozilla/5.0 (U; Linux i645 x86_64; en-US) AppleWebKit/601.16 (KHTML, like Gecko) Chrome/49.0.1408.176 Safari/535
Mozilla/5.0 (Windows; Windows NT 10.0; Win64; x64) AppleWebKit/603.32 (KHTML, like Gecko) Chrome/47.0.2786.173 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_3_2) AppleWebKit/534.18 (KHTML, like Gecko) Chrome/52.0.1890.248 Safari/600
Mozilla/5.0 (Macintosh; Intel Mac OS X 9_8_4; en-US) AppleWebKit/535.42 (KHTML, like Gecko) Chrome/51.0.2713.105 Safari/536
Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/534.11 (KHTML, like Gecko) Chrome/49.0.2883.365 Safari/537
Mozilla/5.0 (U; Linux x86_64) AppleWebKit/603.7 (KHTML, like Gecko) Chrome/53.0.2882.389 Safari/536
Mozilla/5.0 (Windows; Windows NT 6.2; WOW64; en-US) AppleWebKit/533.42 (KHTML, like Gecko) Chrome/50.0.1920.379 Safari/537
Mozilla/5.0 (Linux i580 ) AppleWebKit/536.32 (KHTML, like Gecko) Chrome/50.0.2450.329 Safari/603
Mozilla/5.0 (Linux x86_64) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/52.0.3149.305 Safari/601
Mozilla/5.0 (Windows; Windows NT 6.1; Win64; x64) AppleWebKit/603.27 (KHTML, like Gecko) Chrome/55.0.3956.354 Safari/535
Mozilla/5.0 (Windows; U; Windows NT 10.3; x64) AppleWebKit/533.17 (KHTML, like Gecko) Chrome/52.0.1978.281 Safari/535
Mozilla/5.0 (Windows; Windows NT 10.5; WOW64; en-US) AppleWebKit/602.37 (KHTML, like Gecko) Chrome/55.0.1975.302 Safari/534
Mozilla/5.0 (Windows; U; Windows NT 10.0; Win64; x64) AppleWebKit/601.47 (KHTML, like Gecko) Chrome/52.0.1957.353 Safari/600
Mozilla/5.0 (Windows; Windows NT 10.4; Win64; x64; en-US) AppleWebKit/601.34 (KHTML, like Gecko) Chrome/52.0.3854.364 Safari/600
Mozilla/5.0 (Linux; Linux x86_64) AppleWebKit/537.45 (KHTML, like Gecko) Chrome/55.0.1348.400 Safari/534
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_8) AppleWebKit/603.22 (KHTML, like Gecko) Chrome/54.0.2471.332 Safari/603
Mozilla/5.0 (Macintosh; Intel Mac OS X 8_4_7; en-US) AppleWebKit/600.8 (KHTML, like Gecko) Chrome/49.0.2153.235 Safari/533
Mozilla/5.0 (Linux i546 ) AppleWebKit/601.19 (KHTML, like Gecko) Chrome/47.0.3373.102 Safari/601
Mozilla/5.0 (Linux i675 x86_64) AppleWebKit/603.16 (KHTML, like Gecko) Chrome/47.0.2985.303 Safari/533
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_0) AppleWebKit/536.39 (KHTML, like Gecko) Chrome/53.0.3142.106 Safari/603
Mozilla/5.0 (U; Linux i555 x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/47.0.2486.114 Safari/537
Mozilla/5.0 (Windows; U; Windows NT 10.3; x64; en-US) AppleWebKit/535.46 (KHTML, like Gecko) Chrome/54.0.3121.218 Safari/535
Mozilla/5.0 (Windows; U; Windows NT 6.2;) AppleWebKit/601.18 (KHTML, like Gecko) Chrome/55.0.3771.286 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_8; en-US) AppleWebKit/603.43 (KHTML, like Gecko) Chrome/49.0.3124.173 Safari/533
Mozilla/5.0 (Windows; U; Windows NT 10.3;; en-US) AppleWebKit/537.47 (KHTML, like Gecko) Chrome/47.0.1661.344 Safari/534
Mozilla/5.0 (Windows; Windows NT 6.0; Win64; x64) AppleWebKit/602.15 (KHTML, like Gecko) Chrome/51.0.1901.393 Safari/601
Mozilla/5.0 (Windows; U; Windows NT 10.3; x64; en-US) AppleWebKit/600.10 (KHTML, like Gecko) Chrome/55.0.3373.237 Safari/601
Mozilla/5.0 (Linux; U; Linux i661 ; en-US) AppleWebKit/534.26 (KHTML, like Gecko) Chrome/53.0.1689.129 Safari/536
Mozilla/5.0 (Windows; Windows NT 6.0; x64) AppleWebKit/601.50 (KHTML, like Gecko) Chrome/51.0.1537.286 Safari/536
Mozilla/5.0 (U; Linux x86_64) AppleWebKit/534.11 (KHTML, like Gecko) Chrome/49.0.1482.388 Safari/602
Mozilla/5.0 (Linux; U; Linux i540 x86_64) AppleWebKit/601.16 (KHTML, like Gecko) Chrome/54.0.2820.307 Safari/533
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/533.12 (KHTML, like Gecko) Chrome/55.0.1611.114 Safari/603
Mozilla/5.0 (Linux; Linux x86_64) AppleWebKit/533.20 (KHTML, like Gecko) Chrome/51.0.1830.176 Safari/603
Mozilla/5.0 (Linux i562 x86_64; en-US) AppleWebKit/537.24 (KHTML, like Gecko) Chrome/47.0.2111.292 Safari/601
Mozilla/5.0 (Windows; U; Windows NT 10.0;; en-US) AppleWebKit/533.23 (KHTML, like Gecko) Chrome/50.0.3909.189 Safari/536
Mozilla/5.0 (U; Linux i650 x86_64) AppleWebKit/536.28 (KHTML, like Gecko) Chrome/49.0.2859.226 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_10_3) AppleWebKit/602.16 (KHTML, like Gecko) Chrome/51.0.3813.368 Safari/600
Mozilla/5.0 (Windows; U; Windows NT 6.1;; en-US) AppleWebKit/601.26 (KHTML, like Gecko) Chrome/51.0.2109.130 Safari/601
Mozilla/5.0 (Windows NT 6.1;; en-US) AppleWebKit/600.41 (KHTML, like Gecko) Chrome/47.0.3114.205 Safari/537
Mozilla/5.0 (Windows NT 6.0;; en-US) AppleWebKit/536.8 (KHTML, like Gecko) Chrome/50.0.2772.112 Safari/601
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_0_2; en-US) AppleWebKit/602.27 (KHTML, like Gecko) Chrome/47.0.2350.146 Safari/603
Mozilla/5.0 (Windows NT 6.0; x64; en-US) AppleWebKit/536.25 (KHTML, like Gecko) Chrome/49.0.1754.354 Safari/602
Mozilla/5.0 (Windows; U; Windows NT 10.5; Win64; x64; en-US) AppleWebKit/536.22 (KHTML, like Gecko) Chrome/48.0.3049.106 Safari/536
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_4_4; en-US) AppleWebKit/534.45 (KHTML, like Gecko) Chrome/53.0.1119.345 Safari/534
Mozilla/5.0 (Windows; U; Windows NT 10.4; Win64; x64) AppleWebKit/534.26 (KHTML, like Gecko) Chrome/47.0.3778.368 Safari/600
Mozilla/5.0 (Windows; U; Windows NT 6.0;) AppleWebKit/533.48 (KHTML, like Gecko) Chrome/49.0.3626.114 Safari/601
Mozilla/5.0 (Windows NT 10.2; WOW64) AppleWebKit/533.31 (KHTML, like Gecko) Chrome/52.0.1041.170 Safari/602
Mozilla/5.0 (Macintosh; Intel Mac OS X 8_1_1) AppleWebKit/534.38 (KHTML, like Gecko) Chrome/48.0.3007.131 Safari/600
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_3_1) AppleWebKit/602.8 (KHTML, like Gecko) Chrome/51.0.1144.330 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5) AppleWebKit/601.45 (KHTML, like Gecko) Chrome/49.0.3966.353 Safari/602
Mozilla/5.0 (Windows NT 6.1; WOW64; en-US) AppleWebKit/601.25 (KHTML, like Gecko) Chrome/49.0.1902.358 Safari/536
Mozilla/5.0 (Windows; Windows NT 6.2; x64; en-US) AppleWebKit/601.47 (KHTML, like Gecko) Chrome/51.0.2726.196 Safari/601
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8_8; en-US) AppleWebKit/602.20 (KHTML, like Gecko) Chrome/47.0.2230.286 Safari/600
Mozilla/5.0 (Macintosh; Intel Mac OS X 9_8_0) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/53.0.2271.240 Safari/534
Mozilla/5.0 (Windows NT 10.2;; en-US) AppleWebKit/603.46 (KHTML, like Gecko) Chrome/53.0.3546.324 Safari/533
Mozilla/5.0 (Linux; Linux x86_64) AppleWebKit/536.42 (KHTML, like Gecko) Chrome/55.0.3327.304 Safari/600
Mozilla/5.0 (Windows; U; Windows NT 10.1; WOW64) AppleWebKit/600.34 (KHTML, like Gecko) Chrome/53.0.2595.238 Safari/603
Mozilla/5.0 (Windows; Windows NT 6.1; WOW64; en-US) AppleWebKit/600.9 (KHTML, like Gecko) Chrome/48.0.1208.152 Safari/534
Mozilla/5.0 (Windows; Windows NT 6.1; WOW64) AppleWebKit/601.3 (KHTML, like Gecko) Chrome/49.0.3434.257 Safari/535
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_3; en-US) AppleWebKit/536.14 (KHTML, like Gecko) Chrome/54.0.1658.270 Safari/600
Mozilla/5.0 (Linux x86_64) AppleWebKit/600.16 (KHTML, like Gecko) Chrome/48.0.3691.218 Safari/536
Mozilla/5.0 (Macintosh; Intel Mac OS X 7_3_4) AppleWebKit/533.44 (KHTML, like Gecko) Chrome/50.0.2668.217 Safari/536
Mozilla/5.0 (Windows NT 10.2; Win64; x64; en-US) AppleWebKit/603.7 (KHTML, like Gecko) Chrome/49.0.1259.248 Safari/601
Mozilla/5.0 (Linux; U; Linux i654 x86_64; en-US) AppleWebKit/534.31 (KHTML, like Gecko) Chrome/51.0.1362.279 Safari/603`
).split('\n').filter(Boolean) as string[];
function ua() {
    return UA[Math.floor(Math.random() * UA.length)];
}

export {
    UA,
    ua
}
