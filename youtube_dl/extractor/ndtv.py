# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import (
    compat_urllib_parse_unquote_plus
)
from ..utils import (
    parse_duration,
    remove_end,
    unified_strdate,
    js_to_json,
    int_or_none,
    clean_html,
)


class NDTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www|profit)\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'https://www.ndtv.com/video/news/news/delhi-s-air-quality-status-report-after-diwali-is-very-poor-470372',
            'info_dict': {
                'id': '470372',
                'ext': 'mp4',
                'upload_date': '20171020',
                'description': 'md5:55913730fddd2299bb548e2a47b26a23',
                'title': 'Delhi\'s Air Quality Status Report After Diwali is \'Very Poor\''
            }
        },
        {
            'url': 'https://www.ndtv.com/video/shows/walk-the-talk/walk-the-talk-with-george-fernandes-aired-june-2003-287880',
            'info_dict': {
                'id': '287880',
                'ext': 'mp4',
                'upload_date': '20190129',
                'description': 'md5:dee5565829e91f31c5f7fc66ce69da08',
                'title': 'Walk The Talk With George Fernandes (Aired: June 2003)',
            }
        },
        {
            'url': 'http://profit.ndtv.com/videos/news/video-indian-economy-on-very-solid-track-international-monetary-fund-chief-470040',
            'info_dict': {
                'id': '470040',
                'ext': 'mp4',
                'upload_date': '20171015',
                'description': 'md5:15599329ad2f87cd88c248e7eef46f80',
                'title': 'Indian Economy On \'Very Solid Track\': International Monetary Fund Chief',
            }
        }
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        playerdata_str = self._search_regex(
            # hacky method -- a proper way would be to have a json parser which stop on encountering closing curly brace
            r'__html5playerdata\s*=\s*(.+?),\s*__right_margin_top',
            webpage, 'playerdata', default=None, fatal=False)
        if playerdata_str is not None:
            playerdata_json = self._parse_json(js_to_json(playerdata_str), 'playerdata_json', fatal=False) or {}
            upload_date = unified_strdate(self._html_search_meta(
                'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
                'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
                r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))
            # upload_date = playerdata_json['date']
            return {
                'id': playerdata_json.get('id'),
                'url': playerdata_json.get('media_mp4') or playerdata_json.get('media'),
                'title': playerdata_json.get('title'),
                'description': playerdata_json.get('description'),
                'duration': int_or_none(playerdata_json.get('dur')),
                'upload_date': upload_date,
                'thumbnail': self._og_search_thumbnail(webpage)
            }
        else:
            return {}


class NDTVKhabarIE(InfoExtractor):
    _VALID_URL = r'https?://khabar\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'https://khabar.ndtv.com/video/show/prime-time/prime-time-ill-system-and-poor-education-468818',
            'md5': '78efcf3880ef3fd9b83d405ca94a38eb',
            'info_dict': {
                'id': '468818',
                'ext': 'mp4',
                'title': "प्राइम टाइम: सिस्टम बीमार, स्कूल बदहाल",
                'description': 'md5:de6008f2439005344c1c0c686032b43a',
                'upload_date': '20170928',
                'duration': 2218,
                'thumbnail': r're:https?://.*\.jpg',
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        playerdata_str = self._search_regex(
            # hacky method -- a proper way would be to have a json parser which stops on encountering closing curly brace
            r'__html5playerdata\s*=\s*(.+?)\s*;\s*if',
            webpage, 'playerdata', default=None, fatal=False)
        if playerdata_str is not None:
            playerdata_json = self._parse_json(js_to_json(playerdata_str), 'playerdata_json', fatal=False) or {}
            upload_date = unified_strdate(self._html_search_meta(
                'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
                'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
                r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))
            # upload_date = playerdata_json['date']
            return {
                'id': playerdata_json.get('id'),
                'url': playerdata_json.get('media_mp4') or playerdata_json.get('media'),
                'title': playerdata_json.get('title'),
                'description': playerdata_json.get('description'),
                'duration': int_or_none(playerdata_json.get('dur')),
                'upload_date': upload_date,
                'thumbnail': self._og_search_thumbnail(webpage)
            }
        else:
            return {}


class NDTVAutoIE(InfoExtractor):
    _VALID_URL = r'https?://auto\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'https://auto.ndtv.com/videos/the-cnb-daily-october-13-2017-469935',
            'info_dict': {
                'id': '469935',
                'ext': 'mp4',
                'upload_date': '20171013',
                'description': 'md5:08bdc191cecf4deead40c650c674f8e9',
                'title': 'The CNB Daily - October 13, 2017',
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        playerdata_str = self._search_regex(
            r'videoPlayerScript\((.+?)\);',
            webpage.replace('\n', ' '), 'playerdata', default=None, fatal=False)
        if playerdata_str is not None:
            playerdata_json = self._parse_json(js_to_json(playerdata_str), 'playerdata_json', fatal=False) or {}
            upload_date = unified_strdate(self._html_search_meta(
                'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
                'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
                r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))
            # upload_date = playerdata_json['date']
            return {
                'id': playerdata_json.get('id'),
                'url': playerdata_json.get('filePath'),
                'title': compat_urllib_parse_unquote_plus(playerdata_json.get('title')),
                'description': compat_urllib_parse_unquote_plus(playerdata_json.get('description')),
                'duration': int_or_none(playerdata_json.get('duration')),
                'upload_date': upload_date,
                'thumbnail': self._og_search_thumbnail(webpage)
            }
        else:
            return {}


class NDTVMoviesFoodSwirlsterIE(InfoExtractor):
    _VALID_URL = r'https?://(?:movies|food|swirlster)\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'http://movies.ndtv.com/videos/cracker-free-diwali-wishes-from-karan-johar-kriti-sanon-other-stars-470304',
            'md5': 'f1d709352305b44443515ac56b45aa46',
            'info_dict': {
                'id': '470304',
                'ext': 'mp4',
                'title': "Cracker-Free Diwali Wishes From Karan Johar, Kriti Sanon & Other Stars",
                'description': 'md5:f115bba1adf2f6433fa7c1ade5feb465',
                'upload_date': '20171019',
                'duration': 137,
                'thumbnail': r're:https?://.*\.jpg',
            }
        },
        {
            'url': 'https://food.ndtv.com/video-how-to-make-palak-pakoda-at-home-503346',
            'info_dict': {
                'id': '503346',
                'ext': 'mp4',
                'upload_date': '20190109',
                'description': 'md5:b77c39049dbe185a6bd6c9cd94f3588f',
                'title': 'How To Make Palak Pakoda At Home',
            }
        },
        {
            'url': 'https://swirlster.ndtv.com/video/how-to-make-friends-at-work-469324',
            'info_dict': {
                'id': '469324',
                'ext': 'mp4',
                'upload_date': '20171005',
                'description': 'Ladies, we just made making friends at work way simpler for you!',
                'title': 'How To Make Friends At Work!',
            }
        }
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        playerdata_str = self._search_regex(
            # hacky method -- a proper way would be to have a json parser which stops on encountering closing curly brace
            r'__html5playerdata\s*=\s*(.+),\s*__html5',
            webpage.replace('\n', ' '), 'playerdata', default=None, fatal=False)
        if playerdata_str is not None:
            playerdata_json = self._parse_json(js_to_json(playerdata_str), 'playerdata_json', fatal=False) or {}
            upload_date = unified_strdate(self._html_search_meta(
                'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
                'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
                r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))
            # upload_date = playerdata_json['date']
            return {
                'id': playerdata_json.get('id'),
                'url': playerdata_json.get('media'),
                'title': compat_urllib_parse_unquote_plus(playerdata_json.get('title')),
                'description': compat_urllib_parse_unquote_plus(playerdata_json.get('description')),
                'duration': int_or_none(playerdata_json.get('dur')),
                'upload_date': upload_date,
                'thumbnail': self._og_search_thumbnail(webpage)
            }
        else:
            return {}


class NDTVSportsIE(InfoExtractor):
    _VALID_URL = r'https?://sports\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'https://sports.ndtv.com/cricket/videos/2nd-t20i-rock-thrown-at-australia-cricket-team-bus-after-win-over-india-469764',
            'info_dict': {
                'id': '469764',
                'ext': 'mp4',
                'upload_date': '20171011',
                'description': 'md5:01890be797710959956f5cc7ff9f8841',
                'title': '2nd T20I: Rock Thrown at Australia Cricket Team Bus After Win Over India',
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        playerdata_str = self._search_regex(
            r'__html5playerdata\s*=\s*(.+?)\s*var\s+__by_line',
            webpage.replace('\n', ' '), 'playerdata', default=None, fatal=False)
        if playerdata_str is not None:
            playerdata_json = self._parse_json(js_to_json(playerdata_str), 'playerdata_json', fatal=False) or {}
            upload_date = unified_strdate(self._html_search_meta(
                'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
                'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
                r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))
            # upload_date = playerdata_json['date']
            return {
                'id': playerdata_json.get('id'),
                'url': playerdata_json.get('media'),
                'title': playerdata_json.get('title'),
                'description': playerdata_json.get('description'),
                'duration': parse_duration(playerdata_json.get('dur')),
                'upload_date': upload_date,
                'thumbnail': self._og_search_thumbnail(webpage)
            }
        else:
            return {}


class NDTVGadgetsIE(InfoExtractor):
    _VALID_URL = r'https?://gadgets\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'http://gadgets.ndtv.com/videos/uncharted-the-lost-legacy-review-465568',
            'info_dict': {
                'id': '465568',
                'ext': 'mp4',
                'upload_date': '20170816',
                'description': 'md5:efa289d96ca60db118763c24fee6b295',
                'title': 'Uncharted: The Lost Legacy Review',
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        playerdata_str = self._search_regex(
            r'__html5playerdata\s*=\s*(.+?);\s*var\s*__right',
            webpage.replace('\n', ' '), 'playerdata', default=None, fatal=False)
        if playerdata_str is not None:
            playerdata_json = self._parse_json(js_to_json(playerdata_str), 'playerdata_json', fatal=False) or {}
            upload_date = unified_strdate(self._html_search_meta(
                'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
                'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
                r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))
            # upload_date = playerdata_json['date']
            return {
                'id': playerdata_json.get('id'),
                'url': playerdata_json.get('media'),
                'title': playerdata_json.get('title'),
                'description': playerdata_json.get('description'),
                'duration': parse_duration(playerdata_json.get('dur')),
                'upload_date': upload_date,
                'thumbnail': self._og_search_thumbnail(webpage)
            }
        else:
            return {}


class NDTVDoctorIE(InfoExtractor):
    _VALID_URL = r'https?://doctor\.ndtv\.com/(?:[^/]+/)*videos?/?(?:[^/]+/)*[^/?^&]+-(?P<id>\d+)'

    _TESTS = [
        {
            'url': 'https://doctor.ndtv.com/videos/top-health-stories-of-the-week-467396',
            'info_dict': {
                'id': '467396',
                'ext': 'mp4',
                'upload_date': '20170909',
                'description': 'md5:e6775da155f14a1be31b878b2db39ff3',
                'title': 'Top Health Stories Of The Week',
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # NOTE: Cannot use the json as it can contain contain js code.  For example:
        #             "rtmp": true / false,

        title = compat_urllib_parse_unquote_plus(
            self._search_regex(r"\"title\"\s*:\s*\"([^\"]+)\"", webpage, 'title', default=None) or
            self._og_search_title(webpage))

        video_url = self._search_regex(
            r"\"media\"\s*:\s*\"([^\"]+)\"", webpage, 'video filename')

        duration = parse_duration(self._search_regex(
            r"\"dur\"s*:\s*\"([^\"]+)\"", webpage, 'duration', fatal=False))

        upload_date = unified_strdate(self._html_search_meta(
            'publish-date', webpage, 'upload date', default=None) or self._html_search_meta(
            'uploadDate', webpage, 'upload date', default=None) or self._search_regex(
            r'datePublished"\s*:\s*"([^"]+)"', webpage, 'upload date', fatal=False))

        description = clean_html(remove_end(self._og_search_description(webpage), ' (Read more)'))
        print description

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'description': description,
            'thumbnail': self._og_search_thumbnail(webpage),
            'duration': duration,
            'upload_date': upload_date,
        }
