from regtech_data_validator.create_schemas import validate_phases
from io import BytesIO
import pandas as pd

async def upload_to_storage(lei: str, submission_id: str, content: bytes):
    # implement uploading process here
    pass


async def validate_submission(lei: str, submission_id: str, content: bytes):
    df = pd.read_csv(BytesIO(content), dtype=str, na_filter=False)
    result = validate_phases(df, {"lei": lei})
    # Persist resulting dataframe to tables
