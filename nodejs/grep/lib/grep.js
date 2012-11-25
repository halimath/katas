module.exports.grepSync = function (needle, haystack) {
    if (!needle) {
        throw new Error('needle must not be null or empty');
    }

    return (haystack || []).filter(function (e) {
        return e.indexOf(needle) !== -1;
    });
};

module.exports.grepAsync = function (needle, haystack, callback) {
    if (!needle) {
        callback(new Error('needle must not be null'), null);
        return;
    }

    callback(null, (haystack || []).filter(function (e) {
        return e.indexOf(needle) !== -1;
    }));
};

