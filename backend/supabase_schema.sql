-- Create attendance table in Supabase
CREATE TABLE IF NOT EXISTS attendance (
    id BIGSERIAL PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    register_number VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Present', 'Absent')),
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on register_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_attendance_register_number ON attendance(register_number);

-- Create index on date for faster date-based queries
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);

-- Create composite index for common queries
CREATE INDEX IF NOT EXISTS idx_attendance_register_date ON attendance(register_number, date);

-- Enable Row Level Security (optional, adjust as needed)
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;

-- Policy to allow all operations (adjust based on your security requirements)
CREATE POLICY "Allow all operations" ON attendance
    FOR ALL
    USING (true)
    WITH CHECK (true);
