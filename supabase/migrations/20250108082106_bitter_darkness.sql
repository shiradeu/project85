/*
  # Research Data Management Schema

  1. New Tables
    - `research_data`
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `title` (text)
      - `description` (text)
      - `category` (text)
      - `notes` (text)
      - `file_url1` (text)
      - `file_url2` (text)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on research_data table
    - Add policies for authenticated users to manage their own data
*/

CREATE TABLE research_data (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users NOT NULL,
  title text NOT NULL,
  description text,
  category text,
  notes text,
  file_url1 text,
  file_url2 text,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE research_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own research data"
  ON research_data
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);