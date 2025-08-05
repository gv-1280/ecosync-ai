# Image processing tools
async def read_image_as_bytes(upload_file):
    contents = await upload_file.read()
    return contents
