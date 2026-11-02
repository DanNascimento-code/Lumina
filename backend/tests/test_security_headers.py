from backend.app.core.middleware import CONTENT_SECURITY_POLICY


def test_content_security_policy_allows_storefront_assets() -> None:
    policy = CONTENT_SECURITY_POLICY
    assert "default-src 'self'" in policy
    assert "script-src 'self'" in policy
    assert "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com" in policy
    assert "img-src 'self' data:" in policy
    assert "connect-src 'self'" in policy
    assert "object-src 'none'" in policy
    assert "frame-ancestors 'none'" in policy
