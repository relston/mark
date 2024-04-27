import mark.llm_request
from IPython import embed

content = """
Describe these images in vivid detail

![So horrifying](https://example.com/image.jpg)

![So beautiful](./image2.jpg)

***GPT Response (model: test_model, agent: pytest)**
Oh god, I can't even look at that first image. It's so horrifying. The second one is so beautiful though.

***User Response**
I know, right? I can't believe how different they are.
"""

def test_parse_markdown_content(mock_file):
    with mock_file('./image2.jpg', b"some random string") as mock_open:
        llm_request = mark.llm_request.parse_markdown_content(content)

        assert llm_request.body == content
        
        assert llm_request.images[0].url == 'https://example.com/image.jpg'
        assert llm_request.images[1].url == 'data:image/jpeg;base64,c29tZSByYW5kb20gc3RyaW5n'
        mock_open.assert_called_with("./image2.jpg", 'rb')

        assert llm_request.to_payload() == [
            {'type': 'text', 'text': content}, 
            {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.jpg'}}, 
            {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,c29tZSByYW5kb20gc3RyaW5n'}}
        ]
    