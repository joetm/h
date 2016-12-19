# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from h.services.annotation_stats import AnnotationStatsService
from h.services.annotation_stats import annotation_stats_factory


class TestAnnotationStatsService(object):
    @pytest.mark.usefixtures('user')
    def test_user_annotation_counts_returns_count_of_annotations_for_user(self, svc, user, factories, db_session):
        for i in range(3):
            factories.Annotation(userid=user.userid, shared=True)
        for i in range(2):
            factories.Annotation(userid=user.userid, shared=False)
        for i in range(4):
            factories.Annotation(userid=user.userid, groupid='abc', shared=True)

        results = svc.user_annotation_counts(user.userid)

        assert results['public'] == 3
        assert results['private'] == 2
        assert results['group'] == 4

    def test_annotation_count_returns_count_of_shared_annotations_for_group(self, svc, db_session, group, factories):
        pubid = 'abc123'
        for i in range(3):
            factories.Annotation(groupid=pubid, shared=True)
        for i in range(2):
            factories.Annotation(groupid=pubid, shared=False)

        assert svc.group_annotation_count(pubid) == 3

    @pytest.fixture
    def group(self, user, factories):
        return factories.Group(name='Donkey Trust',
                               authority='foobar.com',
                               creator=user)

    @pytest.fixture
    def user(self, db_session, factories):
        user = factories.User(username='steve',
                              email='steve@steveo.com',
                              authority='example.com',
                              password='stevespassword')
        db_session.add(user)
        db_session.flush()
        return user


class TestAnnotationStatsFactory(object):
    def test_returns_service(self):
        svc = annotation_stats_factory(mock.Mock(), mock.Mock())

        assert isinstance(svc, AnnotationStatsService)

    def test_sets_session(self):
        request = mock.Mock()
        svc = annotation_stats_factory(mock.Mock(), request)

        assert svc.session == request.db


@pytest.fixture
def svc(db_session):
    return AnnotationStatsService(session=db_session)
