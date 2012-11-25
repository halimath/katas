var expect = require('chai').expect;

var grep = require('../lib/grep');

describe('grepSync: ', function () {
    it('should throw error when needle is null', function () {
        expect(function () {
            grep.grepSync(null, null);
        }).to.throw(Error);
    });

    it('should return empty array when haystack is null', function () {
        expect(grep.grepSync('needle', null).length).to.equal(0);
    });

    it('should return empty array when haystack does not contain needle', function () {
        expect(grep.grepSync('needle', ['foo']).length).to.equal(0);
    });

    it('should return array containing needle when haystack contains needle', function () {
        var actual = grep.grepSync('needle', ['needle']);
        expect(actual.length).to.equal(1);
        expect(actual[0]).to.equal('needle');
    });

    it('should return array containing needle when haystack contains needle and other elements', function () {
        var actual = grep.grepSync('needle', ['foo', 'needle', 'bar']);
        expect(actual.length).to.equal(1);
        expect(actual[0]).to.equal('needle');
    });

    it('should return array containing elements that contain needle when haystack contains element with needle and other elements', function () {
        var actual = grep.grepSync('needle', ['foo', 'I am your needle', 'bar']);
        expect(actual.length).to.equal(1);
        expect(actual[0]).to.equal('I am your needle');
    });
});

describe('grepAsync: ', function () {
    describe('Invoking function with needle of null', function () {
        var error = null;
        var result = null;

        before(function (done) {
            grep.grepAsync(null, null, function (err, r) {
                error = err;
                result = r;
                done();
            });
        });

        it('should given an error', function () {
            expect(error).not.to.be.null;
        });
    });

    describe('Invoking function with haystack of null', function () {
        var error = null;
        var result = null;

        before(function (done) {
            grep.grepAsync('needle', null, function (err, r) {
                error = err;
                result = r;
                done();
            });
        });

        it('should given no error', function () {
            expect(error).to.be.null;
        });

        it('should result in empty array', function () {
            expect(result.length).to.equal(0);
        });
    });

    describe('Invoking function with haystack containing needle', function () {
        var error = null;
        var result = null;

        before(function (done) {
            grep.grepAsync('needle', ['needle'], function (err, r) {
                error = err;
                result = r;
                done();
            });
        });

        it('should given no error', function () {
            expect(error).to.be.null;
        });

        it('should result in array containing needle', function () {
            expect(result.length).to.equal(1);
            expect(result[0]).to.equal('needle');
        });
    });

    describe('Invoking function with haystack containing needle and other elements', function () {
        var error = null;
        var result = null;

        before(function (done) {
            grep.grepAsync('needle', ['foo', 'needle', 'bar'], function (err, r) {
                error = err;
                result = r;
                done();
            });
        });

        it('should given no error', function () {
            expect(error).to.be.null;
        });

        it('should result in array containing only needle', function () {
            expect(result.length).to.equal(1);
            expect(result[0]).to.equal('needle');
        });
    });

    describe('Invoking function with haystack containing element with needle and other elements', function () {
        var error = null;
        var result = null;

        before(function (done) {
            grep.grepAsync('needle', ['foo', 'my needle', 'bar'], function (err, r) {
                error = err;
                result = r;
                done();
            });
        });

        it('should given no error', function () {
            expect(error).to.be.null;
        });

        it('should result in array containing only needle', function () {
            expect(result.length).to.equal(1);
            expect(result[0]).to.equal('my needle');
        });
    });
});
