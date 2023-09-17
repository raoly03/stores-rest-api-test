from starter_code.models.user import UserModel
from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as c:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = c.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                self.auth_header = "JWT {}".format(json.loads(auth_request.data)['access_token'])

    def test_item_no_auth(self):
        with self.app() as c:
            r = c.get('/item/test')
            self.assertEqual(r.status_code, 401)

    def test_item_not_found(self):
        with self.app() as c:
            r = c.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(r.status_code, 404)

    def test_item_found(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.get('/item/test', headers={'Authorization': self.auth_header})

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(r.data))

    def test_delete_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.delete('/item/test')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'message': 'Item deleted'},
                                     d2=json.loads(r.data))

    def test_create_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1})
                           , headers={'Content-Type': 'application/json'})

                self.assertEqual(r.status_code, 201)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(r.data))

    def test_create_duplicate_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                c.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                       headers={'Content-Type': 'application/json'})
                r = c.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                           headers={'Content-Type': 'application/json'})

                self.assertEqual(r.status_code, 400)

    def test_put_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.put('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1})
                          , headers={'Content-Type': 'application/json'})

                self.assertEqual(r.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(r.data))

    def test_put_update_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                c.put('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                      headers={'Content-Type': 'application/json'})
                r = c.put('/item/test', data=json.dumps({'price': 18.99, 'store_id': 1}),
                          headers={'Content-Type': 'application/json'})

                self.assertEqual(r.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 18.99)

    def test_item_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.get('/items')

                self.assertDictEqual(d1={'items': [{'name': 'test', 'price': 17.99}]},
                                     d2=json.loads(r.data))
