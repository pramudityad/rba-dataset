# mock_fhir.py
class MockFHIRClient:
    def __init__(self):
        self.dummy_patient_data = {
            "resourceType": "Patient",
            "id": "example_patient_id",
            "name": [{"use": "official", "family": "Doe", "given": ["John"]}],
            "gender": "male",
            "birthDate": "1990-01-01"
        }

    def get_patient(self, patient_id):
        if patient_id == self.dummy_patient_data["id"]:
            return self.dummy_patient_data
        else:
            return {"error": f"Patient with ID {patient_id} not found."}

    def create_observation(self, patient_id, prediction):
        dummy_observation = {
            "resourceType": "Observation",
            "status": "final",
            "category": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "laboratory",
                    "display": "Laboratory"
                }]
            }],
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "1975-2",
                    "display": "Prediction Result"
                }]
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "valueQuantity": {
                "value": prediction,
                "unit": "class",
                "system": "http://unitsofmeasure.org",
                "code": "{classz r szr ssza}"
            }
        }
        return dummy_observation