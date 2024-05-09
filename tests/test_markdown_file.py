from mark.markdown_file import MarkdownFile

markdown_content = """
This is a sample markdown file.

Local image:
![Local Image](./images/sample.png)

Remote image:
![Remote Image](https://example.com/image.png)

Relative image outside directory:
![Outside Image](../images/outside.png)

External url link:
[External URL](https://example.com)

Local link:
[Local Link](./local.md)

Relative link outside directory:
[Outside Link](../outside.md)
"""

# Expected image paths based on the markdown file's hypothetical location
expected_images = [
    {
        'alt': 'Local Image',
        'src': './images/sample.png',
        'image_path': 'path/to/docs/images/sample.png',
    },
    {
        'alt': 'Remote Image',
        'src': 'https://example.com/image.png',
        'image_path': 'https://example.com/image.png',
    },
    {
        'alt': 'Outside Image',
        'src': '../images/outside.png',
        'image_path': 'path/to/images/outside.png',
    }
]

def test_image_paths_resolution(mock_file):
    markdown_file_path = 'path/to/docs/markdown.md'
    
    with mock_file(markdown_file_path, markdown_content):
        with open(markdown_file_path, 'r', encoding='UTF-8') as file:
            md_file = MarkdownFile(file)

            assert md_file.file_path == markdown_file_path
            assert md_file.content == markdown_content

            resolved_images = md_file.images
            # Checking if each dictionary in the list matches the expected results
            assert all(img in resolved_images for img in expected_images)

expected_links = [
    {'text': 'External URL', 'url': 'https://example.com'},
    {'text': 'Local Link', 'url': 'path/to/docs/local.md'},
    {'text': 'Outside Link', 'url': 'path/to/outside.md'}
]

def test_links_extraction(mock_file):
    markdown_file_path = 'path/to/docs/markdown.md'

    with mock_file(markdown_file_path, markdown_content):
        with open(markdown_file_path, 'r', encoding='UTF-8') as file:
            md_file = MarkdownFile(file)

            assert md_file.file_path == markdown_file_path
            assert md_file.content == markdown_content

            extracted_links = md_file.links
            # Checking if each dictionary in the list matches the expected results
            assert all(link in expected_links for link in extracted_links)