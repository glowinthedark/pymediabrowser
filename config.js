URL_TRANSFORMATIONS = [
    // LINK REGEX                                        MATCHING LINK REPLACEMENT
    [/clo_(\d{3}).*\.mp3/i,                              "../PDF/CLO_$1_Vocab.pdf"],
    // chinesepod content links (pdf, html)
    [/(.*chinesepod.*?)(?:_ex)?\.(pdf|html?)/i,          "../$1pr.aac"],
    // chinesepod media links (aac, mp3..)
    [/(.*chinesepod.*?)(?:(dg|pr|rv))?\.(aac|mp3|m4a)/i, "pdf/$1.pdf"],

    // chinese pod collection
    [/(.*?)pr+([^\.]+)\.mp3/i, "$1$2.pdf"],
    [/([^\s,-]+)\b([^\.]+)\.(pdf)/i, "$1pr$2.mp3"]
    // [/(.*).pdf/i,                     function (match, capture) {
    //     return match.replace(/-/g, ' ') + ' ';
    // }]
];
