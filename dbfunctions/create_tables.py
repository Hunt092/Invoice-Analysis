
query = """BEGIN;

CREATE TABLE IF NOT EXISTS public.vendor_details
(
    vendor_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    street character varying,
    city character varying,
    state character varying,
    country character varying,
    zip_code character varying,
    name character varying NOT NULL,
    phone character varying,
    gstin character varying NOT NULL,
    pan character varying,
    PRIMARY KEY (vendor_id)
);

CREATE TABLE IF NOT EXISTS public.receiver_details
(
    receiver_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    street character varying,
    city character varying,
    state character varying,
    country character varying,
    zip_code character varying,
    name character varying NOT NULL,
    phone character varying,
    gstin character varying NOT NULL,
    pan character varying,
    PRIMARY KEY (receiver_id)
);

CREATE TABLE IF NOT EXISTS public.invoice_details
(
    invoice_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    receiver_id integer,
    vendor_id integer,
    order_date character varying,
    invoice_recipt_id character varying NOT NULL,
    total integer NOT NULL,
    PRIMARY KEY (invoice_id),
    CONSTRAINT receiver_id FOREIGN KEY (receiver_id) 
    REFERENCES public.receiver_details (receiver_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID,
    CONSTRAINT vendor_id FOREIGN KEY (vendor_id)
    REFERENCES public.vendor_details (vendor_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID
);

CREATE TABLE IF NOT EXISTS public.line_item_details
(
    line_item_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    invoice_id integer NOT NULL,
    serial_number integer,
    item_description character varying NOT NULL,
    product_code character varying,
    quantity integer NOT NULL,
    additional_amount integer,
    product_price integer,
    total_price integer NOT NULL,
    PRIMARY KEY (line_item_id),
    CONSTRAINT invoice_id FOREIGN KEY (invoice_id)
    REFERENCES public.invoice_details (invoice_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID
);

END;"""


def createTables(conn):
    cursor = conn.cursor()
    cursor.execute(query)
    
    print('Data tables created.....')

