import os
from datetime import datetime
import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from .calendar_schema import Appointment

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
def get_dynamodb_client():
    """Get the DynamoDB client based on environment"""
    # Check if we're running in AWS environment or local
    if 'AWS_EXECUTION_ENV' in os.environ:
        # Production - use default endpoint
        return boto3.resource('dynamodb')
    else:
        # Local development
        endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')
        if endpoint_url:
            return boto3.resource('dynamodb', endpoint_url=endpoint_url)
        else:
            # Default to AWS
            return boto3.resource('dynamodb')

# Table name from environment or default
TABLE_NAME = os.environ.get('APPOINTMENTS_TABLE_NAME', 'TherastackAppointments')

def create_appointment(appt: Appointment):
    """Create a new appointment"""
    try:
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table(TABLE_NAME)
        
        item = appt.model_dump()
        
        # Generate ID if not provided
        if not item.get('appointment_id'):
            item['appointment_id'] = f"appt-{uuid.uuid4().hex[:8]}"
            
        # Convert datetime to string
        if isinstance(item['start_time'], datetime):
            item['start_time'] = appt.start_time.isoformat()
            
        if isinstance(item['end_time'], datetime):
            item['end_time'] = appt.end_time.isoformat()
            
        # Put item in DynamoDB
        table.put_item(Item=item)
        
        return {"message": "Appointment created", "appointment_id": item['appointment_id']}
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        raise Exception(f"Error creating appointment: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Error creating appointment: {str(e)}")

def get_appointment(appointment_id: str):
    """Get an appointment by ID"""
    try:
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table(TABLE_NAME)
        
        response = table.get_item(
            Key={'appointment_id': appointment_id}
        )
        
        return response.get('Item')
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        raise Exception(f"Error retrieving appointment: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Error retrieving appointment: {str(e)}")

def list_appointments_by_therapist(therapist_id: str):
    """List appointments by therapist ID using GSI"""
    try:
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table(TABLE_NAME)
        
        # Query using GSI
        response = table.query(
            IndexName='TherapistIndex',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('therapist_id').eq(therapist_id)
        )
        
        return response.get('Items', [])
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        raise Exception(f"Error listing appointments: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Error listing appointments: {str(e)}")

def list_appointments_by_patient(patient_id: str):
    """List appointments by patient ID using GSI"""
    try:
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table(TABLE_NAME)
        
        # Query using GSI
        response = table.query(
            IndexName='PatientIndex',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('patient_id').eq(patient_id)
        )
        
        return response.get('Items', [])
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        raise Exception(f"Error listing appointments: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Error listing appointments: {str(e)}")
        
def list_all_appointments():
    """List all appointments - use with caution in production"""
    try:
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table(TABLE_NAME)
        
        response = table.scan()
        data = response.get('Items', [])
        
        # Handle pagination for large datasets
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response.get('Items', []))
            
        return data
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        raise Exception(f"Error listing appointments: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Error listing appointments: {str(e)}")
        
def update_appointment_status(appointment_id: str, status: str):
    """Update appointment status"""
    try:
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table(TABLE_NAME)
        
        # Update the item
        response = table.update_item(
            Key={'appointment_id': appointment_id},
            UpdateExpression="set #status = :s",
            ExpressionAttributeNames={
                '#status': 'status'
            },
            ExpressionAttributeValues={
                ':s': status
            },
            ReturnValues="UPDATED_NEW"
        )
        
        return response.get('Attributes', {"status": status})
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        raise Exception(f"Error updating appointment: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise Exception(f"Error updating appointment: {str(e)}")