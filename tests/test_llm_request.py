import mark.llm_request

def test_from_markdown_file(mock_file, mock_markdown_file):
    with mock_file('./image2.jpg', b"some random string") as mock_open:
        llm_request = mark.llm_request.from_markdown_file(mock_markdown_file)

        assert llm_request.body == mock_markdown_file.content
        
        assert llm_request.images[0].url == 'https://example.com/image.jpg'
        assert llm_request.images[1].url == 'data:image/jpeg;base64,c29tZSByYW5kb20gc3RyaW5n'
        

        assert llm_request.to_payload() == [
            {'type': 'text', 'text': mock_markdown_file.content}, 
            {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.jpg'}}, 
            {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,c29tZSByYW5kb20gc3RyaW5n'}}
        ]
    


def test_from_markdown_file(mock_file, mock_markdown_file):
    with mock_file('./image2.jpg', b"some random string") as mock_open:
        llm_request = mark.llm_request.from_markdown_file(mock_markdown_file)

        assert llm_request.body == mock_markdown_file.content
        
        assert llm_request.images[0].url == 'https://example.com/image.jpg'
        assert llm_request.images[1].url == 'data:image/jpeg;base64,c29tZSByYW5kb20gc3RyaW5n'
        

        assert llm_request.to_payload() == [
            {'type': 'text', 'text': mock_markdown_file.content}, 
            {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.jpg'}}, 
            {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,c29tZSByYW5kb20gc3RyaW5n'}}
        ]
    