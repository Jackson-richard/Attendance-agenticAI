# Installation Notes

## Windows Installation Workaround

Due to compilation requirements on Windows (specifically the `pyroaring` dependency needed by Supabase's storage module), we've modified the code to use PostgREST directly instead of the full Supabase client.

### What Was Changed

1. **supabase_client.py**: Modified to use `SyncPostgrestClient` from `postgrest` package instead of the full `supabase` client
2. This avoids the need for Microsoft Visual C++ Build Tools
3. We only need database operations, not storage or realtime features

### Installed Packages

The following packages are installed and working:
- fastapi
- uvicorn[standard]
- pydantic
- langgraph
- langchain
- langchain-openai
- python-dotenv
- python-multipart
- postgrest (for database operations)
- supabase-auth, supabase-functions, realtime (minimal installs to satisfy imports)

### What's NOT Installed

- `storage3` and `pyroaring` - These require C++ compilation and aren't needed for database operations

### Testing

The backend should work correctly for attendance database operations. The PostgREST client provides the same database functionality as the full Supabase client.

### If You Need Storage Features Later

If you need Supabase storage features in the future, you'll need to install Microsoft Visual C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/
