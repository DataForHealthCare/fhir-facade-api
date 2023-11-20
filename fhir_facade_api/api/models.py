from uuid import uuid4
from pandas import json_normalize
from dataclasses import dataclass
from datetime import datetime
from .static.column_data import data
from .static.columns import columns
import pandas as pd 
import json
import time
import os


# FHIR Default Values
@dataclass
class CareDetail:
    facility_identifier_value: str = ''
    facility_identifier_system: str = 'http://127.0.0.1:5000/claims/facilities'
    
@dataclass
class CareTeam:
    provider_reference: str = 'placeholder'
    sequence: str = 1

@dataclass 
class ClaimDetail:
    created: str = ''
    enterer_identifier_value: str = 'placeholder'
    identifier_value: str = ''
    subtype_coding_code: str = 'placeholder'
    total_value: int = 0
    type_coding_code: str = 'placeholder'
    enterer_identifier_system: str = 'http://127.0.0.1:5000/claims/enterer'
    identifier_system: str = 'http://127.0.0.1:5000/claims/identifier'
    status: str = 'active'
    subtype_coding_system: str = 'http://127.0.0.1:5000/claims/claims-subtype'
    total_currency: str = 'USD'
    type_coding_system: str = 'http://127.0.0.1:5000/claims/claim-type'
    use: str = 'claim'

@dataclass
class Diagnosis:
    diagnosiscodeableconcept_coding_code: str = 'placeholder'
    sequence: str = 'placeholder'
    diagnosiscodeableconcept_coding_system: str = 'http://127.0.0.1:5000/claims/diagnosis-codeable-concept'

@dataclass
class Insurance:
    coverage_reference: str = 'placeholder'
    focal: bool = True
    sequence: str = 1
   
@dataclass
class Item:
    careteamsequence: str = 1
    encounter_reference: str = 'placeholder'
    net_value: int = 0
    productorservice_coding_code: str = 'placeholder'
    sequence: str = 1
    serviced_date: str = ''
    unit_price_value: int = 0
    net_currency: str = 'USD'
    productorservice_coding_system: str = 'http://127.0.0.1:5000/claims'
    unit_price_currency: str = 'USD'

@dataclass
class MetaData:
    id_: str = ''
    last_updated: str = ''
    resource_type: str = 'Claim'
    tag_code: str = 'actionable'
    tag_display: str = 'Actionable'
    tag_system: str = 'http://127.0.0.1:5000/claims/resources'
    version_id: str = '1'

@dataclass
class Narrative:
    div: str = ''
    status: str = 'generated'
    
@dataclass
class Patient:
    patient_reference: str = 'placeholder'

@dataclass
class Procedure:
    date: str = 'placeholder'
    procedureodeableconcept_coding_code: str = 'placeholder' 
    sequence: str = 1
    text: str = 'placeholder'
    type_coding_code: str = 'placeholder'
    udi_reference: str = 'placeholder' 
    procedureodeableconcept_coding_system: str = 'http://127.0.0.1:5000/claims/procedure-codeable-concept'
    type_coding_system: str = 'http://127.0.0.1:5000/claims/procedure-type'
    
@dataclass
class Provider:
    insurer_reference: str = 'placeholder'
    payee_type_coding_code: str = 'placeholder'
    priority_coding_code: str = 'placeholder'
    provider_reference: str = 'placeholder'
    payee_type_coding_system: str = 'http://127.0.0.1:5000/claims/payee'
    priority_coding_system: str = 'http://127.0.0.1:5000/claims/priority-code'
       

class LastUpdated:
    FILE = 'C:\\Users\\f9656\\Desktop\\fhir_facade\\api\\static\\fhir_facade_schema.json'

    def __init__(self):
        self.modified_time = os.path.getmtime(self.FILE)
        self.meta_last_updated = time.ctime(self.modified_time)

    def metadata(self):
        last_updated_date = self.meta_last_updated.replace(' ', '-')
        return last_updated_date

class TransformData(
    CareDetail,
    CareTeam,
    ClaimDetail,
    Diagnosis,
    Insurance,
    Item,
    LastUpdated,
    MetaData,
    Patient,
    Procedure
):
    def __init__(self):
        self.system_id = [str(uuid4()) for _ in range(len(columns))]
        self.last_updated_date = LastUpdated()
        self.fhir_data = []
        self.row_idx = 0
          
    def transform_fhir_data(self): 
        row_idx = self.row_idx
        for row in data:
            with open("C:\\Users\\f9656\\Desktop\\fhir_facade\\api\\static\\fhir_facade_schema.json", "r") as json_file:
                fhir_schema = json.load(json_file)
                fhir_schema['id'] = self.system_id[row_idx]
                fhir_schema['identifier'][0]['value'] = str(row[0])
                fhir_schema['created'] = str(row[1].date())
                fhir_schema['facility']['identifier']['value'] = str(row[2])
                fhir_schema['diagnosis'][0]['diagnosisCodeableConcept']['coding'][0][Diagnosis.diagnosiscodeableconcept_coding_code] = str(row[3])
                fhir_schema['item'][0]['servicedDate'] = str(row[4].date())
                fhir_schema['meta']['lastUpdated'] = self.last_updated_date.metadata()
                self.fhir_data.append(fhir_schema)  
                fhir_schema['text']['div'] = self.narrative_html(self.fhir_data[row_idx]) 

                '''Default Dataclass Values'''
                # Care Detail
                fhir_schema['facility']['identifier']['system'] = CareDetail.facility_identifier_system

                # Care Team
                fhir_schema['careTeam'][0]['provider']['reference'] = CareTeam.provider_reference
                fhir_schema['careTeam'][0]['sequence'] = CareTeam.sequence

                # Claim Detail
                fhir_schema['enterer']['identifier']['system'] = ClaimDetail.enterer_identifier_system
                fhir_schema['enterer']['identifier']['value'] = ClaimDetail.enterer_identifier_value
                fhir_schema['subType']['coding'][0]['code'] = ClaimDetail.subtype_coding_code
                fhir_schema['subType']['coding'][0]['system'] = ClaimDetail.subtype_coding_system
                fhir_schema['type']['coding'][0]['code'] = ClaimDetail.type_coding_code
                fhir_schema['type']['coding'][0]['system'] = ClaimDetail.type_coding_system
                fhir_schema['identifier'][0]['system'] = ClaimDetail.identifier_system
                fhir_schema['total']['currency'] = ClaimDetail.total_currency
                fhir_schema['total']['value'] = ClaimDetail.total_value
                fhir_schema['status'] = ClaimDetail.status
                fhir_schema['use'] = ClaimDetail.use

                # Diagnosis
                fhir_schema['diagnosis'][0]['diagnosisCodeableConcept']['coding'][0]['code'] = Diagnosis.diagnosiscodeableconcept_coding_code 
                fhir_schema['diagnosis'][0]['diagnosisCodeableConcept']['coding'][0]['system'] = Diagnosis.diagnosiscodeableconcept_coding_system 
                fhir_schema['diagnosis'][0]['sequence'] = Diagnosis.sequence

                # Insurance
                fhir_schema['insurance'][0]['focal'] = Insurance.focal
                fhir_schema['insurance'][0]['sequence'] = Insurance.sequence 
                fhir_schema['insurance'][0]['coverage']['reference'] = Insurance.coverage_reference

                # Item
                fhir_schema['item'][0]['sequence'] = Item.sequence
                fhir_schema['item'][0]['careTeamSequence'].append(Item.careteamsequence)
                fhir_schema['item'][0]['encounter'][0]['reference'] = Item.encounter_reference  
                fhir_schema['item'][0]['net']['value'] = Item.net_value
                fhir_schema['item'][0]['net']['currency'] = Item.net_currency
                fhir_schema['item'][0]['productOrService']['coding'][0]['code'] = Item.productorservice_coding_code
                fhir_schema['item'][0]['productOrService']['coding'][0]['system'] = Item.productorservice_coding_system
                fhir_schema['item'][0]['unitPrice']['value'] = Item.unit_price_value
                fhir_schema['item'][0]['unitPrice']['currency'] = Item.unit_price_currency

                # MetaData
                fhir_schema['resourceType'] = MetaData.resource_type
                fhir_schema['meta']['tag'][0]['code'] = MetaData.tag_code
                fhir_schema['meta']['tag'][0]['display'] = MetaData.tag_display
                fhir_schema['meta']['tag'][0]['system'] = MetaData.tag_system
                fhir_schema['meta']['versionId'] = MetaData.version_id
                
                # Narrative
                fhir_schema['text']['status'] = Narrative.status

                # Patient
                fhir_schema['patient']['reference'] = Patient.patient_reference

                # Procedure
                fhir_schema['procedure'][0]['date'] = Procedure.date
                fhir_schema['procedure'][0]['sequence'] = Procedure.sequence
                fhir_schema['procedure'][0]['text'] = Procedure.text
                fhir_schema['procedure'][0]['udi'][0]['reference'] = Procedure.udi_reference
                fhir_schema['procedure'][0]['type'][0]['coding'][0]['system'] = Procedure.type_coding_system
                fhir_schema['procedure'][0]['type'][0]['coding'][0]['code'] = Procedure.type_coding_code
                fhir_schema['procedure'][0]['procedureCodeableConcept']['coding'][0]['code'] = Procedure.procedureodeableconcept_coding_code
                fhir_schema['procedure'][0]['procedureCodeableConcept']['coding'][0]['system'] = Procedure.procedureodeableconcept_coding_system
                fhir_schema['procedure'][0]['procedureCodeableConcept']['text'] = Procedure.text

                # Provider
                fhir_schema['insurer']['reference'] = Provider.insurer_reference
                fhir_schema['provider']['reference'] = Provider.provider_reference
                fhir_schema['payee']['type']['coding'][0]['code'] = Provider.payee_type_coding_code
                fhir_schema['payee']['type']['coding'][0]['system'] = Provider.payee_type_coding_system
                fhir_schema['priority']['coding'][0]['code'] = Provider.priority_coding_code
                fhir_schema['priority']['coding'][0]['system'] = Provider.priority_coding_system
        
            row_idx += 1
        return self.fhir_data

    def narrative_html(self, fhir_data: list=''):
        df = json_normalize(fhir_data)

        user_view_fhir_claim = {
            'Id': [],
            'ClaimNumber': [],
            'CreatedDate': [],
            'Patient': [],
            'Facility': [],
            'ClaimTotal': []
        }

        for _, row in df.iterrows():
            user_view_fhir_claim['Id'].append(row['id'])
            user_view_fhir_claim['ClaimNumber'].append(row['identifier'][0]['value'])
            date = datetime.strptime(row['created'], '%Y-%m-%d')
            _date = date.strftime("%b %d, %Y")
            user_view_fhir_claim['CreatedDate'].append(_date)
            user_view_fhir_claim['Patient'].append(row['patient.reference'])
            user_view_fhir_claim['Facility'].append(row['facility.identifier.value'])
            user_view_fhir_claim['ClaimTotal'].append(row['total.value'])
        html = self.dataframe_to_html(user_view_fhir_claim)
        final_html = self.remove_html_space(html)
        return final_html

    def dataframe_to_html(self, user_view: dict = ''):
        html_df = pd.DataFrame(user_view)
        html_claim = html_df.to_html(index=False)
        return html_claim
    
    def remove_html_space(self, html: str = ''):
        fhir_html = ''.join(html.split())
        rendered_fhir_html = '{}'.format(fhir_html)
        return rendered_fhir_html
    
