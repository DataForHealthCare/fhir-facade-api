from flask_restful import Resource, abort
from flask import request
from .models import TransformData


# Global Data
def transformed_data():
    transform_data = TransformData()
    api_data = transform_data.transform_fhir_data()
    return api_data

data_out = transformed_data()

# Methods for Views
class ViewMethods:
    def results_not_found_response(self):
        return abort(404, message="Results not found.")

    def response(self, response_data):
        if request.method == 'GET':
            if response_data == []:
                self.results_not_found_response()
            return response_data
        
# Root View
class Root(Resource):
    def get(self):
        return 'FHIR Facade API'
    
 # Search Method : claims
class ClaimsView(Resource, ViewMethods):
    def get(self):
        response_data = data_out
        return self.response(response_data)

# Search Method : id
class IdView(Resource, ViewMethods):
    def get(self, unique_id):
        response_data =  [_ for _ in data_out if _['id'] == unique_id]
        return self.response(response_data)
              
# Search Method : identifier
class IdentifierView(Resource, ViewMethods):
    def get(self, identifier):
        response_data = [_ for _ in data_out if _['identifier'][0]['value'] == identifier]
        return self.response(response_data)

# Search Method : service-date  
class ServicedDateView(Resource, ViewMethods):
    def get(self, service_date):
        response_data =  [_ for _ in data_out if _['item'][0]['servicedDate']  == service_date]
        return self.response(response_data)
        
# Search Method : created  
class CreatedView(Resource, ViewMethods):
    def get(self, created_date):
        response_data =  [_ for _ in data_out if _['created'] == created_date]
        return self.response(response_data)
             
# Parameter Search
class SearchView(Resource, ViewMethods):
    def __init__(self) -> None:
        super().__init__()
        self.results = []
        self.unique = []
        self.duplicates = []
        self.count = {}
        self.claims = []
  
    def get(self, data_=data_out):
        request_data = request.args
        req_data = dict(request_data)

        self.find_duplicate_parameters(req_data, request_data)
      
        for claim in data_:
            for key, _ in request_data.items():
                query_string_lst = key.split('.')
                returned_value = self.search(claim, query_string_lst)
                returned_value = self.cast_to_string(returned_value)
                self.results_response(returned_value)
                if returned_value == _:
                    self.results.append(claim)

        self.sort_unique_results()
        self.results_hash_map()
        self.unanimous_query_reuslt(request_data)
   
        if len(request_data) == 1:
            return self.response(self.unique)
        return self.response(self.claims)
            
    def results_response(self, claim_element):
        if claim_element is None:
            return self.results_not_found_response()
    
    def cast_to_string(self, claim_element):
        if isinstance(claim_element, int):
            return str(claim_element)
        return claim_element

    def search(self, query, keys):
        lst_idx = 0
        lst_len = len(keys)
        for key in keys:
            lst_idx += 1
            if key not in query:
                return None
            for k, v in query.items():
                if k == key:
                    if isinstance(v, dict):
                        return self.search(v, keys[1:])
                    if isinstance(v, list):
                        for _ in v:
                            if isinstance(_, dict):
                                return self.search(_, keys[1:])
                    if lst_idx != lst_len:
                        return None
                    return v
                     
    def sort_unique_results(self):
        for i in self.results:
            if i not in self.unique:
                self.unique.append(i)
            else:
                self.duplicates.append(i)

    def results_hash_map(self):
        for z in self.duplicates:
            if z['id'] not in self.count:
                self.count[z['id']] = 1
            else:
                self.count[z['id']] += 1

    def unanimous_query_reuslt(self, request_data):
        for k, v in self.count.items():
            if v + 1 == len(request_data):
                for i in self.duplicates:
                    if i['id'] == k \
                        and i not in self.claims:
                        self.claims.append(i)

    def find_duplicate_parameters(self, req_data, request_data):
        count_keys = 0
        for key in request_data:
            count_keys += len(request_data.getlist(key))
        if count_keys > len(req_data):
            return self.results_not_found_response()
