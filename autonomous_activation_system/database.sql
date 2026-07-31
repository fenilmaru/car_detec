-- ============================================================
-- Autonomous Activation System - PostgreSQL Database Schema
-- Enterprise AI Vehicle Safety & Autonomous Monitoring Platform
-- ============================================================

-- Create Database
-- CREATE DATABASE autonomous_activation_db;
-- \c autonomous_activation_db;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- AUTHENTICATION & ROLES
-- ============================================================

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT DEFAULT '',
    permissions JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    password VARCHAR(256) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) DEFAULT '',
    last_name VARCHAR(150) DEFAULT '',
    email VARCHAR(254) DEFAULT '',
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    role_id UUID REFERENCES roles(id) ON DELETE SET NULL,
    phone VARCHAR(20) DEFAULT '',
    avatar VARCHAR(100) DEFAULT '',
    is_verified BOOLEAN DEFAULT FALSE,
    last_login_ip INET,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    address TEXT DEFAULT '',
    city VARCHAR(100) DEFAULT '',
    state VARCHAR(100) DEFAULT '',
    country VARCHAR(100) DEFAULT '',
    zip_code VARCHAR(20) DEFAULT '',
    emergency_contact_name VARCHAR(200) DEFAULT '',
    emergency_contact_phone VARCHAR(20) DEFAULT '',
    blood_group VARCHAR(5) DEFAULT '',
    date_of_birth DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    object_id VARCHAR(100) DEFAULT '',
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- VEHICLES
-- ============================================================

CREATE TABLE vehicle_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT DEFAULT '',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_type_id UUID NOT NULL REFERENCES vehicle_types(id) ON DELETE PROTECT,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    color VARCHAR(50) DEFAULT '',
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vin VARCHAR(17) UNIQUE NOT NULL,
    registration_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    current_mileage DECIMAL(10,2) DEFAULT 0,
    fuel_type VARCHAR(20) DEFAULT 'gasoline',
    has_ai_camera BOOLEAN DEFAULT FALSE,
    has_gps BOOLEAN DEFAULT FALSE,
    insurance_expiry DATE,
    registration_expiry DATE,
    last_service_date DATE,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_vehicle_status CHECK (status IN ('active', 'maintenance', 'inactive', 'retired')),
    CONSTRAINT chk_fuel_type CHECK (fuel_type IN ('gasoline', 'diesel', 'electric', 'hybrid', 'cng', 'lpg'))
);

CREATE INDEX idx_vehicles_license ON vehicles(license_plate);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_make_model ON vehicles(make, model);

CREATE TABLE vehicle_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    document_type VARCHAR(20) NOT NULL,
    file VARCHAR(100) NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    is_valid BOOLEAN DEFAULT TRUE,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_doc_type CHECK (document_type IN ('registration', 'insurance', 'inspection', 'permit', 'other'))
);

CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    start_location VARCHAR(500) DEFAULT '',
    end_location VARCHAR(500) DEFAULT '',
    start_latitude DECIMAL(10,7),
    start_longitude DECIMAL(10,7),
    end_latitude DECIMAL(10,7),
    end_longitude DECIMAL(10,7),
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'scheduled',
    distance_km DECIMAL(8,2) DEFAULT 0,
    duration_minutes INTEGER DEFAULT 0,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_trip_status CHECK (status IN ('scheduled', 'active', 'completed', 'cancelled'))
);

CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_trips_vehicle_time ON trips(vehicle_id, start_time);

CREATE TABLE trip_routes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    speed DECIMAL(5,2) DEFAULT 0,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_trip_routes_trip_time ON trip_routes(trip_id, timestamp);

-- ============================================================
-- DRIVERS
-- ============================================================

CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_class VARCHAR(10) NOT NULL,
    license_issue_date DATE NOT NULL,
    license_expiry_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    total_trips INTEGER DEFAULT 0,
    total_distance_km DECIMAL(10,2) DEFAULT 0,
    safety_score DECIMAL(5,2) DEFAULT 100.00,
    last_trip_date DATE,
    photo VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_driver_status CHECK (status IN ('active', 'suspended', 'inactive', 'on_leave')),
    CONSTRAINT chk_license_class CHECK (license_class IN ('A', 'B', 'C', 'D', 'CDL'))
);

CREATE INDEX idx_drivers_license ON drivers(license_number);
CREATE INDEX idx_drivers_status ON drivers(status);

CREATE TABLE driver_health (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    blood_pressure VARCHAR(20) DEFAULT '',
    heart_rate INTEGER,
    vision_test BOOLEAN,
    last_checkup DATE,
    medical_conditions TEXT DEFAULT '',
    medications TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- ACCIDENTS
-- ============================================================

CREATE TABLE accidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'reported',
    location VARCHAR(500) DEFAULT '',
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    speed_at_impact DECIMAL(5,2),
    weather_conditions VARCHAR(100) DEFAULT '',
    road_conditions VARCHAR(100) DEFAULT '',
    description TEXT DEFAULT '',
    ai_detected BOOLEAN DEFAULT FALSE,
    emergency_notified BOOLEAN DEFAULT FALSE,
    police_notified BOOLEAN DEFAULT FALSE,
    ambulance_notified BOOLEAN DEFAULT FALSE,
    reported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_acc_severity CHECK (severity IN ('minor', 'moderate', 'severe', 'critical', 'fatal')),
    CONSTRAINT chk_acc_status CHECK (status IN ('reported', 'investigating', 'resolved', 'closed'))
);

CREATE INDEX idx_accidents_severity ON accidents(severity);
CREATE INDEX idx_accidents_status ON accidents(status);
CREATE INDEX idx_accidents_vehicle ON accidents(vehicle_id, reported_at);

CREATE TABLE accident_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    accident_id UUID NOT NULL REFERENCES accidents(id) ON DELETE CASCADE,
    image VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    is_ai_analyzed BOOLEAN DEFAULT FALSE,
    ai_analysis JSONB DEFAULT '{}',
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE accident_videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    accident_id UUID NOT NULL REFERENCES accidents(id) ON DELETE CASCADE,
    video VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    duration_seconds INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- EMERGENCY
-- ============================================================

CREATE TABLE emergency_contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(254) DEFAULT '',
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sos_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    alert_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    location VARCHAR(500) DEFAULT '',
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    description TEXT DEFAULT '',
    auto_triggered BOOLEAN DEFAULT FALSE,
    manual_triggered BOOLEAN DEFAULT FALSE,
    notified_contacts BOOLEAN DEFAULT FALSE,
    notified_emergency_services BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_alert_type CHECK (alert_type IN ('accident', 'medical', 'breakdown', 'security', 'fire', 'other')),
    CONSTRAINT chk_alert_status CHECK (status IN ('active', 'responding', 'resolved', 'dismissed'))
);

CREATE INDEX idx_sos_status ON sos_alerts(status);
CREATE INDEX idx_sos_type ON sos_alerts(alert_type);

CREATE TABLE emergency_services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    service_type VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(254) DEFAULT '',
    address TEXT NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_svc_type CHECK (service_type IN ('ambulance', 'police', 'fire', 'hospital', 'tow_truck'))
);

-- ============================================================
-- GPS & TRACKING
-- ============================================================

CREATE TABLE gps_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    altitude DECIMAL(8,2),
    speed DECIMAL(5,2) DEFAULT 0,
    heading DECIMAL(5,2),
    accuracy DECIMAL(5,2),
    battery_level INTEGER,
    ignition_on BOOLEAN DEFAULT TRUE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_gps_vehicle_time ON gps_locations(vehicle_id, timestamp);
CREATE INDEX idx_gps_timestamp ON gps_locations(timestamp);

CREATE TABLE route_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    trip_id UUID REFERENCES trips(id) ON DELETE SET NULL,
    start_latitude DECIMAL(10,7) NOT NULL,
    start_longitude DECIMAL(10,7) NOT NULL,
    end_latitude DECIMAL(10,7),
    end_longitude DECIMAL(10,7),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    total_distance_km DECIMAL(8,2) DEFAULT 0,
    avg_speed DECIMAL(5,2) DEFAULT 0,
    max_speed DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- CAMERA & AI DETECTIONS
-- ============================================================

CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) DEFAULT '',
    stream_url VARCHAR(200) DEFAULT '',
    status VARCHAR(20) DEFAULT 'offline',
    is_active BOOLEAN DEFAULT TRUE,
    last_frame_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_camera_loc CHECK (location IN ('front', 'rear', 'left', 'right', 'interior', 'dash')),
    CONSTRAINT chk_camera_status CHECK (status IN ('online', 'offline', 'maintenance'))
);

CREATE TABLE detection_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    camera_id UUID REFERENCES cameras(id) ON DELETE SET NULL,
    detection_type VARCHAR(20) NOT NULL,
    severity VARCHAR(20) DEFAULT 'info',
    description TEXT DEFAULT '',
    confidence_score DECIMAL(5,4),
    bounding_boxes JSONB DEFAULT '[]',
    frame_image VARCHAR(100) DEFAULT '',
    metadata JSONB DEFAULT '{}',
    is_reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_det_type CHECK (detection_type IN ('object', 'lane', 'traffic_sign', 'seatbelt', 'drowsiness', 'accident', 'helmet', 'speed')),
    CONSTRAINT chk_det_severity CHECK (severity IN ('info', 'warning', 'critical'))
);

CREATE INDEX idx_det_type_time ON detection_logs(detection_type, created_at);
CREATE INDEX idx_det_severity ON detection_logs(severity);
CREATE INDEX idx_det_vehicle_time ON detection_logs(vehicle_id, created_at);

-- ============================================================
-- NOTIFICATIONS & ALERTS
-- ============================================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(20) DEFAULT 'info',
    priority VARCHAR(20) DEFAULT 'medium',
    is_read BOOLEAN DEFAULT FALSE,
    action_url VARCHAR(200) DEFAULT '',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_notif_type CHECK (notification_type IN ('alert', 'warning', 'info', 'emergency', 'system')),
    CONSTRAINT chk_notif_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
);

CREATE INDEX idx_notif_user_read ON notifications(user_id, is_read);
CREATE INDEX idx_notif_priority ON notifications(priority, created_at);

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    detection_log_id UUID NOT NULL REFERENCES detection_logs(id) ON DELETE CASCADE,
    notification_id UUID NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    resolution_notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE email_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipient VARCHAR(254) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_email_status CHECK (status IN ('sent', 'failed', 'pending'))
);

CREATE TABLE sms_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipient_phone VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_sms_status CHECK (status IN ('sent', 'failed', 'pending'))
);

-- ============================================================
-- AUTO-UPDATE TRIGGERS
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_roles_updated_at BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cameras_updated_at BEFORE UPDATE ON cameras
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_accidents_updated_at BEFORE UPDATE ON accidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_drivers_updated_at BEFORE UPDATE ON drivers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- SEQUENCES
-- ============================================================

CREATE SEQUENCE IF NOT EXISTS seq_detection_id START 1000;
CREATE SEQUENCE IF NOT EXISTS seq_accident_id START 100;
CREATE SEQUENCE IF NOT EXISTS seq_trip_id START 1000;

-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- Roles
INSERT INTO roles (id, name, description, permissions) VALUES
    ('11111111-1111-1111-1111-111111111111', 'Admin', 'Full system access', '{"all": true}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'Fleet Manager', 'Manage vehicles and drivers', '{"vehicles": true, "drivers": true}'::jsonb),
    ('33333333-3333-3333-3333-333333333333', 'Operator', 'View and monitor only', '{"view": true}'::jsonb),
    ('44444444-4444-4444-4444-444444444444', 'Driver', 'Driver access', '{"trips": true}'::jsonb);

-- Users (password: admin123 hashed with PBKDF2)
INSERT INTO users (id, password, username, email, first_name, last_name, is_superuser, is_staff, role_id) VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'pbkdf2_sha256$870000$abc123$placeholder', 'admin', 'admin@aas.com', 'System', 'Admin', true, true, '11111111-1111-1111-1111-111111111111'),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'pbkdf2_sha256$870000$def456$placeholder', 'fleet_manager', 'fleet@aas.com', 'Fleet', 'Manager', false, false, '22222222-2222-2222-2222-222222222222');

-- Vehicle Types
INSERT INTO vehicle_types (id, name) VALUES
    ('aaaa0000-0000-0000-0000-000000000001', 'Sedan'),
    ('aaaa0000-0000-0000-0000-000000000002', 'SUV'),
    ('aaaa0000-0000-0000-0000-000000000003', 'Truck'),
    ('aaaa0000-0000-0000-0000-000000000004', 'Van'),
    ('aaaa0000-0000-0000-0000-000000000005', 'Electric');

-- Emergency Services
INSERT INTO emergency_services (id, name, service_type, phone, address, latitude, longitude) VALUES
    ('eeee0000-0000-0000-0000-000000000001', 'City Ambulance', 'ambulance', '911', '123 Main St, City', 40.7128, -74.0060),
    ('eeee0000-0000-0000-0000-000000000002', 'Police Department', 'police', '911', '456 Police Ave', 40.7580, -73.9855),
    ('eeee0000-0000-0000-0000-000000000003', 'Fire Station #1', 'fire', '911', '789 Fire Rd', 40.7484, -73.9857),
    ('eeee0000-0000-0000-0000-000000000004', 'General Hospital', 'hospital', '555-0100', '321 Health Blvd', 40.7831, -73.9712);

-- Sample Vehicles
INSERT INTO vehicles (id, owner_id, vehicle_type_id, make, model, year, color, license_plate, vin, registration_number, status, fuel_type, has_ai_camera, has_gps) VALUES
    ('vvvv0000-0000-0000-0000-000000000001', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaa0000-0000-0000-0000-000000000001', 'Tesla', 'Model 3', 2024, 'White', 'ABC-1234', '5YJ3E1EA1PF000001', 'REG-001', 'active', 'electric', true, true),
    ('vvvv0000-0000-0000-0000-000000000002', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaa0000-0000-0000-0000-000000000002', 'BMW', 'X5', 2023, 'Black', 'XYZ-5678', '5UXCR6C09P9A00002', 'REG-002', 'active', 'gasoline', true, true),
    ('vvvv0000-0000-0000-0000-000000000003', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'aaaa0000-0000-0000-0000-000000000003', 'Ford', 'F-150', 2023, 'Blue', 'DEF-9012', '1FTFW1E50PFA00003', 'REG-003', 'active', 'gasoline', false, true);
