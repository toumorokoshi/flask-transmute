import json


def test_happy_path(test_app):
    r = test_app.get("/multiply?left=3&right=3")
    assert json.loads(r.data)["result"] == 9


def test_swagger(test_app):
    r = test_app.get("/swagger.json")
    swagger = json.loads(r.data)
    assert swagger == {
        u'info': {
            u'version': u'1.0',
            u'title': u'example'
        },
        u'paths': {
            u'/multiply': {
                u'get': {
                    u'description': u'',
                    u'parameters': [
                        {u'required': False,
                         u'type': u'string',
                         u'name': u'right',
                         u'in': u'query'
                        },
                        {u'required': False,
                         u'type': u'string',
                         u'name': u'left',
                         u'in': u'query'
                        }
                    ],
                    u'produces': [u'application/json',
                                  u'application/x-yaml'],
                    u'summary': u'',
                    u'consumes': [u'application/json',
                                  u'application/x-yaml'],
                    u'responses': {
                        u'200': {
                            u'description': u'success',
                            u'schema': {
                                u'required': [u'success', u'result'],
                                u'type': u'object',
                                u'properties': {
                                    u'result': {u'type': u'number'}, u'success': {u'type': u'boolean'}}, u'title': u'SuccessObject'}}, u'400': {u'description': u'invalid input received', u'schema': {u'required': [u'success', u'message'], u'type': u'object', u'properties': {u'message': {u'type': u'string'}, u'success': {u'type': u'boolean'}}, u'title': u'FailureObject'}}}}}}, u'basePath': u'/', u'swagger': u'2.0'}
